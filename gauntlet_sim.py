from kaggle_environments import make
import time

def run_gauntlet(matches_per_opponent=50):
    # We turn debug=False so it doesn't spam the console
    env = make("cabt", debug=False)
    
    # Your smart agent
    my_agent = "lucario_v2/main.py"
    
    # The Kaggle sample opponents
    opponents = {
        "Baseline Lucario": "opponents/lucario_base/main.py",
        "Dragapult ex": "opponents/dragapult/main.py",
        "Mega Abomasnow ex": "opponents/abomasnow/main.py",
        "Iono": "opponents/iono/main.py"
    }
    
    print(f"🥊 STARTING THE GAUNTLET 🥊")
    print(f"Testing against {len(opponents)} decks. {matches_per_opponent} matches each.")
    print("-" * 40)
    
    total_wins = 0
    total_ties = 0
    total_matches = 0
    
    start_time = time.time()
    
    for opp_name, opp_path in opponents.items():
        print(f"\nVersus: {opp_name}...")
        wins = 0
        losses = 0
        ties = 0
        
        for i in range(1, matches_per_opponent + 1):
            # Alternate who goes first
            if i % 2 != 0:
                steps = env.run([my_agent, opp_path])
                reward_me = steps[-1][0]["reward"]
                reward_opp = steps[-1][1]["reward"]
                status_me = steps[-1][0]["status"]
                status_opp = steps[-1][1]["status"]
            else:
                steps = env.run([opp_path, my_agent])
                reward_me = steps[-1][1]["reward"]
                reward_opp = steps[-1][0]["reward"]
                status_me = steps[-1][1]["status"]
                status_opp = steps[-1][0]["status"]
                
            # --- CRASH HANDLING LOGIC ---
            if reward_me is None and reward_opp is None:
                ties += 1
            elif reward_me is None:
                losses += 1
                # Only print once in a while so we don't spam the console too hard
                if losses == 1: 
                    print(f"    [!] WARNING: Our bot crashed! (Status: {status_me})")
            elif reward_opp is None:
                wins += 1
                if wins == 1:
                    print(f"    [!] WARNING: Opponent crashed! (Status: {status_opp})")
            # --- NORMAL WIN/LOSS LOGIC ---
            elif reward_me > reward_opp:
                wins += 1
            elif reward_opp > reward_me:
                losses += 1
            else:
                ties += 1
                
        # Calculate win rate for this specific matchup
        win_rate = (wins / matches_per_opponent) * 100
        print(f"Result: {wins}W - {losses}L - {ties}T ({win_rate:.1f}% Win Rate)")
        
        total_wins += wins
        total_ties += ties
        total_matches += matches_per_opponent

    end_time = time.time()
    
    # The Final Report Card
    overall_win_rate = (total_wins / total_matches) * 100
    print("\n" + "="*40)
    print("🏆 GAUNTLET RESULTS 🏆")
    print("="*40)
    print(f"Total Matches: {total_matches}")
    print(f"Overall Win Rate: {overall_win_rate:.1f}%")
    print(f"Total Time: {round(end_time - start_time, 2)} seconds")
    print("="*40)

if __name__ == "__main__":
    # You can change the number of matches per deck here
    run_gauntlet(matches_per_opponent=50)