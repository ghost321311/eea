# AI Fish Catching System 🎣

An intelligent AI agent that learns to catch fish autonomously using reinforcement learning and computer vision simulation.

## Features

- **Simulated Fishing Environment**: Realistic water physics and fish behavior
- **AI Agent**: Q-Learning based agent that learns optimal fishing strategies
- **Real-time Visualization**: Watch the AI fish in action
- **Statistics Tracking**: Monitor catch rates, success metrics, and learning progress
- **Configurable Difficulty**: Adjust fish behavior and environmental factors

## Project Structure

```
├── environment/
│   ├── __init__.py
│   └── fishing_env.py      # Main fishing simulation environment
├── agent/
│   ├── __init__.py
│   └── fishing_agent.py    # Q-Learning AI agent
├── utils/
│   ├── __init__.py
│   └── visualization.py    # Rendering and visualization
├── train.py                # Training script
├── play.py                 # Run trained agent
└── requirements.txt
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Train the AI Agent

```bash
python train.py --episodes 1000 --visualize
```

### Run Trained Agent

```bash
python play.py --model saved_model.pkl --render
```

## How It Works

### The Fishing Environment
- Fish spawn randomly in a water body
- Each fish has health, hunger, and behavior patterns
- The AI must cast, wait, and reel at the right moments

### The AI Agent
- Uses **Q-Learning** to learn state-action values
- States: Fish position, distance, time since cast, etc.
- Actions: Cast, Wait, Reel, Move
- Rewards: +100 for successful catch, -1 for wasted time

## Performance Metrics

- Catch Success Rate
- Average Time per Catch
- Learning Efficiency
- Environmental Adaptation
