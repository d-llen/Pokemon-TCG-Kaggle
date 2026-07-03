from kaggle_environments import make
import time

def run_batch(matches=100):
    print(f"Initializing engine for {matches} matches...")
    
    # We turn debug=False so it doesn't spam the console for 100 games
    env = make("cabt", debug=False)
    
    agent_1 = "lucario_test/main.py"
    agent_2 = "lucario_test/main.py"  # You can change this to pit two different versions against each other!
    
    wins_agent_1 = 0
    wins_agent_2 = 0
    ties = 0
    
    start_time = time.time()
    
    for i in range(1, matches + 1):
        # Alternate who gets passed into the engine first
        if i % 2 != 0:
            # Odd matches: Agent 1 is Player 0
            steps = env.run([agent_1, agent_2])
            reward_p0 = steps[-1][0]["reward"]
            reward_p1 = steps[-1][1]["reward"]
            
            if reward_p0 > reward_p1: wins_agent_1 += 1
            elif reward_p1 > reward_p0: wins_agent_2 += 1
            else: ties += 1
            
        else:
            # Even matches: Agent 2 is Player 0 (Swapped!)
            steps = env.run([agent_2, agent_1])
            reward_p0 = steps[-1][0]["reward"] # This is now Agent 2
            reward_p1 = steps[-1][1]["reward"] # This is now Agent 1
            
            if reward_p1 > reward_p0: wins_agent_1 += 1
            elif reward_p0 > reward_p1: wins_agent_2 += 1
            else: ties += 1
            
        if i % 10 == 0 or i == matches:
            print(f"Match {i}/{matches} complete...")

    end_time = time.time()
    
    print("\n" + "="*30)
    print("🏆 BATCH SIMULATION COMPLETE 🏆")
    print("="*30)
    print(f"Total Matches : {matches}")
    print(f"Time Taken    : {round(end_time - start_time, 2)} seconds")
    print(f"Agent 1 Wins  : {wins_agent_1} ({round((wins_agent_1/matches)*100, 1)}%)")
    print(f"Agent 2 Wins  : {wins_agent_2} ({round((wins_agent_2/matches)*100, 1)}%)")
    print(f"Ties          : {ties} ({round((ties/matches)*100, 1)}%)")
    print("="*30)

if __name__ == "__main__":
    # You can change the number of matches here
    run_batch(matches=100)