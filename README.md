# 🎮 Tic-Tac-Toe with Reinforcement Learning.

A retro arcade-style Tic-Tac-Toe game powered by Q-Learning reinforcement learning algorithm. Play against an AI agent that learns and improves through self-play!

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📋 Table of Contents
- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [How to Play](#how-to-play)
- [Reinforcement Learning Explained](#reinforcement-learning-explained)
- [Project Structure](#project-structure)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

- 🤖 **Q-Learning AI Agent** - Learns optimal strategies through self-play
- 🎚️ **Three Difficulty Levels**:
  - **Easy**: Random moves
  - **Medium**: Uses learned Q-table with some exploration
  - **Hard**: Plays optimally using greedy policy
- 🎨 **Retro Arcade UI** - Dark theme with neon colors
- ⚙️ **Customizable Training** - Adjust hyperparameters (alpha, gamma, epsilon)
- 💾 **Save/Load Q-Table** - Preserve trained models
- 🎯 **Interactive Gameplay** - Choose to play as X or O
- 📊 **Training Progress** - Real-time training status updates

---

## 🎬 Demo

### Game Interface
```
┌─────────────────────────────────┐
│     Tic-Tac-Toe RL             v│
│                                 │
│   [X] [ ] [O]                   │
│   [ ] [O] [ ]                   │
│   [ ] [ ] [X]                   │
│                                 │
│  Difficulty: Medium             │
│  Your turn! (X)                 │
└─────────────────────────────────┘
```

---

## 🔧 Installation

### Prerequisites
- Python 3.7 or higher
- No external libraries required (uses only Python standard library!)

### Steps

1. **Clone or Download** the repository:
```bash
git clone https://github.com/yourusername/tictactoe-rl.git
cd tictactoe-rl
```

2. **Verify Python installation**:
```bash
python --version
```

3. **Run the game** (see next section)

---

## 🚀 How to Run

### Method 1: Command Line
```bash
python tictactoe_rl.py
```

### Method 2: VS Code
1. Open the project folder in VS Code
2. Open `tictactoe_rl.py`
3. Press `F5` or click the ▶️ Run button

### Method 3: Double-click (Windows)
1. Right-click `tictactoe_rl.py`
2. Select "Open with" → "Python"

---

## 🎮 How to Play

### Quick Start
1. **Launch the game** using one of the methods above
2. **Choose your symbol**: X (goes first) or O (goes second)
3. **Select difficulty**: Easy, Medium, or Hard
4. **Click "New Game"** to start
5. **Make your move** by clicking on any empty square
6. **Win the game** by getting 3 in a row (horizontal, vertical, or diagonal)!

### Training the AI
1. Click **"Train Agent"** button
2. Set training parameters:
   - **Episodes**: Number of games for training (default: 10,000)
   - **Alpha (α)**: Learning rate (0.0 - 1.0, default: 0.3)
   - **Gamma (γ)**: Discount factor (0.0 - 1.0, default: 0.9)
   - **Epsilon (ε)**: Exploration rate (0.0 - 1.0, default: 0.1)
3. Click **"Start Training"**
4. Wait for training to complete (progress shown in status bar)
5. **Save the Q-table** to preserve the trained model

### Saving and Loading
- **Save Q-Table**: Click "Save Q-Table" to save the trained agent
- **Load Q-Table**: Click "Load Q-Table" to restore a previously trained agent
- **Reset Q-Table**: Click "Reset Q-Table" to clear all learning and start fresh

---

## 🧠 Reinforcement Learning Explained

### What is Q-Learning?

Q-Learning is a model-free reinforcement learning algorithm that learns the value of actions in different states.

### Key Concepts

#### 1. **Q-Table**
A lookup table that stores Q-values for state-action pairs:
```
Q(state, action) = Expected future reward
```

#### 2. **Bellman Equation**
Updates Q-values based on rewards:
```
Q(s,a) ← Q(s,a) + α[r + γ·max Q(s',a') - Q(s,a)]
```

Where:
- **α (alpha)**: Learning rate - How much to update based on new information
- **γ (gamma)**: Discount factor - How much to value future rewards
- **r**: Immediate reward (+1 for win, -1 for loss, 0 for draw)
- **s**: Current state (board configuration)
- **a**: Action taken (position 0-8)

#### 3. **Exploration vs Exploitation**
- **Exploration (ε)**: Try random moves to discover new strategies
- **Exploitation (1-ε)**: Use known best moves from Q-table

### Training Process

1. **Self-Play**: Agent plays against itself for thousands of games
2. **State Representation**: Board is converted to a string key (e.g., "X O XX    ")
3. **Action Selection**: Choose moves using ε-greedy policy
4. **Reward Assignment**:
   - Win: +1.0
   - Loss: -1.0
   - Draw: +0.5
   - Ongoing: 0.0
5. **Q-Value Update**: Update Q-table using Bellman equation
6. **Convergence**: After many episodes, Q-values stabilize to optimal strategy

### Why It Works

Through repeated play, the agent:
- Learns winning patterns (3 in a row)
- Recognizes blocking opportunities
- Discovers optimal opening moves
- Builds a "memory" of good and bad moves

---

## 📁 Project Structure

```
tictactoe-rl/
│
├── tictactoe_rl.py          # Main game file
├── qtable.pkl               # Saved Q-table (generated after training)
├── README.md                # This file
└── PressStart2P-Regular.ttf # Optional retro font (optional)
```

### Code Structure

```python
# Main Components:

1. QLearningAgent Class
   ├── q_table: Dictionary storing Q-values
   ├── choose_action(): Select moves using ε-greedy
   └── update(): Update Q-values using Bellman equation

2. TicTacToeRL Class (GUI)
   ├── build_ui(): Create game interface
   ├── make_move(): Handle player moves
   ├── agent_move(): Handle AI moves
   ├── train_agent(): Self-play training loop
   └── File operations: save/load/reset Q-table
```

---

## ⚙️ Customization

### Adjusting Difficulty

Modify the difficulty behavior in the `agent_move()` method:

```python
if self.difficulty == "Easy":
    move = random.choice(actions)  # Completely random
elif self.difficulty == "Medium":
    move = self.agent.choose_action(self.state, actions)  # Some exploration
else:  # Hard
    move = self.agent.choose_action(self.state, actions, greedy=True)  # Optimal play
```

### Hyperparameter Tuning

Experiment with different values:

| Parameter | Recommended Range | Effect |
|-----------|-------------------|--------|
| Alpha (α) | 0.1 - 0.5 | Higher = faster learning, but less stable |
| Gamma (γ) | 0.8 - 0.99 | Higher = values long-term rewards more |
| Epsilon (ε) | 0.1 - 0.3 | Higher = more exploration during training |
| Episodes | 10,000 - 100,000 | More = better learning, but slower |

### Changing Colors

Edit color values in the `build_ui()` method:

```python
bg="#111"         # Background (dark)
fg="#0ff"         # Text (cyan)
player_fg="#0ff"  # Player X color (cyan)
agent_fg="#f00"   # Agent O color (red)
win_bg="#0f0"     # Winning squares (green)
```

---

## 🐛 Troubleshooting

### Issue: "Python was not found"
**Solution**: 
1. Install Python from [python.org](https://www.python.org/downloads/)
2. Check "Add Python to PATH" during installation
3. Restart your terminal/VS Code

### Issue: Game window is too small/large
**Solution**: Adjust window size in code:
```python
popup.geometry("320x300")  # Change width x height
```

### Issue: Training takes too long
**Solution**: 
- Reduce number of episodes (try 5,000 instead of 10,000)
- Train overnight for better results (50,000+ episodes)

### Issue: AI doesn't play well even after training
**Solution**:
- Train for more episodes (50,000+)
- Adjust alpha to 0.2-0.3 for better learning
- Ensure you saved the Q-table after training

### Issue: Retro font not displaying
**Solution**: 
- The game works without the custom font
- To add it: Download "Press Start 2P" font and place in project folder
- Font is optional - game uses system default if unavailable

---

## 🚀 Future Enhancements

Potential improvements for the project:

- [ ] Add statistics tracking (wins/losses/draws)
- [ ] Implement minimax algorithm for comparison
- [ ] Add sound effects for moves and game events
- [ ] Create neural network version (Deep Q-Learning)
- [ ] Add multiplayer mode (human vs human)
- [ ] Implement different board sizes (4x4, 5x5)
- [ ] Add replay functionality to review past games
- [ ] Create tournament mode with multiple AI agents
- [ ] Export/import Q-tables in different formats
- [ ] Add visualization of Q-values for educational purposes

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

### Contribution Ideas
- Improve UI/UX design
- Add new difficulty levels
- Optimize training algorithm
- Write unit tests
- Improve documentation
- Fix bugs

---

## 📚 References & Resources

### Reinforcement Learning
- [Sutton & Barto - Reinforcement Learning: An Introduction](http://incompleteideas.net/book/the-book.html)
- [Q-Learning Tutorial](https://www.learndatasci.com/tutorials/reinforcement-q-learning-scratch-python-openai-gym/)
- [OpenAI Spinning Up](https://spinningup.openai.com/)

### Python & Tkinter
- [Python Official Documentation](https://docs.python.org/3/)
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [Real Python - Python GUI Programming](https://realpython.com/python-gui-tkinter/)

---

## 📄 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👨‍💻 Authors

- Gautam Girish [@NomadWr3nch](https://github.com/NomadWr3nch)
- Yadunandan V  [@skr-jyr](https://github.com/skr-jyr)
- Yadunandan P [@yadunandan04](https://github.com/yadunandan04)
---

## 🙏 Acknowledgments

- Inspired by classic Tic-Tac-Toe and reinforcement learning research
- Q-Learning algorithm developed by Chris Watkins
- Retro arcade aesthetic inspired by 1980s gaming culture
- Thanks to the Python and open-source community

---

## ⭐ Star This Project!

If you found this project helpful, please consider giving it a star on GitHub! It helps others discover the project.

---

**Made with ❤️ and Python**

*Last Updated: November 2025*
