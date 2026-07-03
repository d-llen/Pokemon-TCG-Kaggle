from kaggle_environments import make
import json

def run_local_match():
    print("Initializing the cabt engine...")
    
    # Create the Pokémon TCG environment
    # debug=True will print engine errors to the console
    env = make("cabt", debug=True)
    
    # Define the paths to the agents. 
    # You can pit the Lucario agent against a copy of itself.
    agent_1 = "lucario_test/main.py"
    agent_2 = "lucario_test/main.py"
    
    print(f"Starting match: {agent_1} VS {agent_2}")
    
    # Run the episode
    steps = env.run([agent_1, agent_2])
    
    print(f"Match concluded in {len(steps)} steps.")
    
    # Determine the winner (the last step contains the final rewards)
    final_rewards = steps[-1][0]["reward"], steps[-1][1]["reward"]
    if final_rewards[0] > final_rewards[1]:
        print("Agent 1 Wins!")
    elif final_rewards[1] > final_rewards[0]:
        print("Agent 2 Wins!")
    else:
        print("It's a Tie!")

    # Optional: Save the game log for debugging
    with open("game_log.json", "w") as f:
        json.dump(steps, f)
        print("Game log saved to game_log.json")

if __name__ == "__main__":
    run_local_match()