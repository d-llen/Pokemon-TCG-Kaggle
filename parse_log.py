import json
import os
from cg.api import to_observation_class, all_card_data, AreaType, OptionType

# 1. Build a dictionary to translate Card IDs (e.g., 678) into English Names
CARD_DB = {c.cardId: c.name for c in all_card_data()}

def get_card_name(obs, area, index, player_idx):
    """Helper to safely fetch a card's actual name based on where it is on the board."""
    try:
        ps = obs.current.players[player_idx]
        card_obj = None
        
        if area == AreaType.HAND: card_obj = ps.hand[index]
        elif area == AreaType.ACTIVE: card_obj = ps.active[index]
        elif area == AreaType.BENCH: card_obj = ps.bench[index]
        elif area == AreaType.DECK: return "A Card from Deck"
        
        if card_obj and hasattr(card_obj, 'id'):
            return CARD_DB.get(card_obj.id, f"Unknown ({card_obj.id})")
    except Exception:
        pass
    return "Unknown Target"

def parse_game_log(log_path="game_log.json"):
    if not os.path.exists(log_path):
        print(f"Could not find {log_path}!")
        return

    with open(log_path, "r") as f:
        steps = json.load(f)

    print(f"--- Loaded Match with {len(steps)} Steps ---\n")

    # Start at step 1 (since step 0 is just the initial setup)
    for i in range(1, len(steps)):
        prev_step = steps[i-1]
        curr_step = steps[i]

        for player_id in [0, 1]:
            actions_taken = curr_step[player_id].get("action")
            
            # Using 'is None' because an action index of '0' is valid!
            if actions_taken is None or actions_taken == []:
                continue
                
            if isinstance(actions_taken, int):
                actions_taken = [actions_taken]

            prev_obs_raw = prev_step[player_id].get("observation")
            if not prev_obs_raw:
                continue
                
            prev_obs = to_observation_class(prev_obs_raw)
            
            if not prev_obs.select or not prev_obs.select.option:
                continue

            for action_idx in actions_taken:
                if action_idx < len(prev_obs.select.option):
                    picked_option = prev_obs.select.option[action_idx]
                    
                    try:
                        action_type = OptionType(picked_option.type).name
                    except Exception:
                        action_type = f"UNKNOWN_{picked_option.type}"
                    
                    message = f"Step {i:03d} | Player {player_id} | "
                    
                    if action_type in ["PLAY", "ATTACH", "EVOLVE"]:
                        card_name = get_card_name(prev_obs, AreaType.HAND, picked_option.index, player_id)
                        message += f"{action_type}: [{card_name}]"
                        
                    elif action_type == "ABILITY":
                        card_name = get_card_name(prev_obs, picked_option.area, picked_option.index, player_id)
                        message += f"{action_type}: [{card_name}]"
                        
                    elif action_type == "CARD":
                        card_name = get_card_name(prev_obs, picked_option.area, picked_option.index, player_id)
                        # Find out WHY the engine asked them to select a card
                        try:
                            context = prev_obs.select.context.name
                            message += f"SELECTED [{card_name}] (Reason: {context})"
                        except:
                            message += f"SELECTED [{card_name}]"
                            
                    elif action_type == "ATTACK":
                        message += f"ATTACKED!"
                    elif action_type == "PASS":
                        message += "Ended Turn."
                    else:
                        message += f"{action_type}"
                    
                    # The missing piece!
                    print(message)

if __name__ == "__main__":
    parse_game_log("game_log.json")