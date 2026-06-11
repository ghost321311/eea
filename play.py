"""
Play script - Run the trained agent
"""

import argparse
import numpy as np
from environment.fishing_env import FishingEnvironment
from agent.fishing_agent import FishingAgent


def play(model_path: str = 'fishing_agent.pkl', num_episodes: int = 5, 
         render: bool = True, max_steps: int = 500):
    """
    Run the trained agent
    
    Args:
        model_path: Path to saved agent model
        num_episodes: Number of episodes to run
        render: Whether to display the environment
        max_steps: Maximum steps per episode
    """
    
    env = FishingEnvironment(water_width=200, water_height=200, 
                             num_fish=5, max_steps=max_steps)
    agent = FishingAgent()
    
    try:
        agent.load(model_path)
    except FileNotFoundError:
        print(f"Model not found at {model_path}")
        print("Train the agent first with: python train.py")
        return
    
    print(f"Running trained agent for {num_episodes} episodes")
    print("=" * 50)
    print()
    
    total_catches = 0
    total_rewards = 0
    episode_details = []
    
    for episode in range(num_episodes):
        state = env.reset()
        done = False
        steps = 0
        episode_reward = 0
        
        print(f"Episode {episode + 1}")
        print("-" * 50)
        
        while not done and steps < max_steps:
            # Get action from trained agent (no exploration)
            action = agent.get_action(state, training=False)
            
            # Execute action
            action_names = ['Cast', 'Wait', 'Reel', 'Move Left', 'Move Right']
            
            next_state, reward, done = env.step(action)
            episode_reward += reward
            state = next_state
            steps += 1
            
            # Print action (less verbose)
            if steps % 10 == 0 or done or reward > 50:
                print(f"Step {steps}: {action_names[action]} | Reward: {reward:+.1f} | Catches: {env.catches}/{env.num_fish}")
        
        total_catches += env.catches
        total_rewards += episode_reward
        episode_details.append({
            'catches': env.catches,
            'reward': episode_reward,
            'steps': steps
        })
        
        print()
        print(f"Episode Summary: {env.catches}/{env.num_fish} fish caught | Total Reward: {episode_reward:.2f}")
        print()
        
        if render:
            print(env.render())
            print()
    
    # Overall statistics
    print("=" * 50)
    print("OVERALL STATISTICS")
    print("=" * 50)
    print(f"Total Episodes: {num_episodes}")
    print(f"Average Catches: {total_catches / num_episodes:.2f}")
    print(f"Total Fish Caught: {total_catches}")
    print(f"Average Reward: {total_rewards / num_episodes:.2f}")
    print(f"Success Rate: {(total_catches / (num_episodes * 5)) * 100:.1f}%")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run trained fishing AI')
    parser.add_argument('--model', type=str, default='fishing_agent.pkl', 
                       help='Path to saved agent model')
    parser.add_argument('--episodes', type=int, default=5, 
                       help='Number of episodes to run')
    parser.add_argument('--render', action='store_true', default=True,
                       help='Display environment')
    parser.add_argument('--max-steps', type=int, default=500,
                       help='Maximum steps per episode')
    
    args = parser.parse_args()
    
    play(
        model_path=args.model,
        num_episodes=args.episodes,
        render=args.render,
        max_steps=args.max_steps
    )
