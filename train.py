"""
Training script - Train the AI agent to catch fish
"""

import sys
import numpy as np
from environment.fishing_env import FishingEnvironment
from agent.fishing_agent import FishingAgent


def train(num_episodes: int = 1000, visualize: bool = False, 
          render_every: int = 100, save_path: str = None):
    """
    Train the fishing agent
    
    Args:
        num_episodes: Number of training episodes
        visualize: Whether to display environment
        render_every: Render every N episodes
        save_path: Path to save the trained model
    """
    
    env = FishingEnvironment(water_width=200, water_height=200, 
                             num_fish=5, max_steps=500)
    agent = FishingAgent(state_size=8, action_size=5, 
                        learning_rate=0.1, discount_factor=0.95)
    
    print("Starting training...")
    print(f"Episodes: {num_episodes}")
    print(f"Visualize: {visualize}")
    print()
    
    for episode in range(num_episodes):
        state = env.reset()
        total_reward = 0
        catches = 0
        done = False
        steps = 0
        
        while not done and steps < 500:
            # Agent selects action
            action = agent.get_action(state, training=True)
            
            # Environment step
            next_state, reward, done = env.step(action)
            
            # Agent learns
            agent.learn(state, action, reward, next_state, done)
            
            state = next_state
            total_reward += reward
            catches = env.catches
            steps += 1
        
        # Record statistics
        agent.episode_rewards.append(total_reward)
        agent.episode_catches.append(catches)
        
        # Decay exploration
        agent.decay_exploration()
        
        # Print progress
        if (episode + 1) % render_every == 0:
            stats = agent.get_stats()
            print(f"Episode {episode + 1}/{num_episodes}")
            print(f"  Last Reward: {total_reward:.2f}")
            print(f"  Avg Reward (last 100): {stats['avg_reward']:.2f}")
            print(f"  Last Catches: {catches}/{env.num_fish}")
            print(f"  Avg Catches (last 100): {stats['avg_catches']:.2f}")
            print(f"  States Explored: {stats['states_explored']}")
            print(f"  Exploration Rate: {stats['exploration_rate']:.4f}")
            print()
            
            if visualize:
                print(env.render())
    
    print("Training complete!")
    
    # Save model
    if save_path:
        agent.save(save_path)
    else:
        agent.save('fishing_agent.pkl')
    
    return agent, env


def evaluate(agent: FishingAgent, num_episodes: int = 10):
    """Evaluate trained agent"""
    env = FishingEnvironment(water_width=200, water_height=200, 
                             num_fish=5, max_steps=500)
    
    print(f"\nEvaluating agent over {num_episodes} episodes...")
    print()
    
    total_catches = 0
    total_rewards = 0
    
    for episode in range(num_episodes):
        state = env.reset()
        done = False
        steps = 0
        
        while not done and steps < 500:
            action = agent.get_action(state, training=False)  # No exploration
            next_state, reward, done = env.step(action)
            state = next_state
            steps += 1
        
        total_catches += env.catches
        total_rewards += sum(agent.episode_rewards[-num_episodes:])
        
        print(f"Episode {episode + 1}: Caught {env.catches}/{env.num_fish} fish")
    
    avg_catches = total_catches / num_episodes
    avg_rewards = total_rewards / num_episodes
    
    print()
    print(f"Average Catches: {avg_catches:.2f}/{env.num_fish}")
    print(f"Average Reward: {avg_rewards:.2f}")
    print()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Train fishing AI agent')
    parser.add_argument('--episodes', type=int, default=1000, help='Number of episodes')
    parser.add_argument('--visualize', action='store_true', help='Visualize training')
    parser.add_argument('--render-every', type=int, default=100, help='Render every N episodes')
    parser.add_argument('--save', type=str, default='fishing_agent.pkl', help='Save path')
    parser.add_argument('--evaluate', action='store_true', help='Evaluate after training')
    
    args = parser.parse_args()
    
    agent, env = train(
        num_episodes=args.episodes,
        visualize=args.visualize,
        render_every=args.render_every,
        save_path=args.save
    )
    
    if args.evaluate:
        evaluate(agent, num_episodes=10)
