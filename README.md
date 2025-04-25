# Galactic Defenders

A modern reimagining of the classic Space Invaders arcade game, built with Python and Tkinter.

![Galactic Defenders](https://github.com/yourusername/galacticdefendersv2/raw/main/screenshots/gameplay.png)

## Project Overview

Galactic Defenders is a retro-style arcade shooter with modern gameplay elements and visual enhancements. In this game, you control a spaceship defending Earth from waves of alien invaders. The game features progressive difficulty, a leaderboard system, and adaptive enemy behavior.

### Key Features

- **Classic Arcade Gameplay**: Control your ship, shoot aliens, and protect Earth
- **Progressive Difficulty**: Face increasingly challenging levels with faster and more aggressive enemies
- **Protective Barriers**: Use strategic cover that degrades as it takes damage
- **Local Leaderboard**: Compete for high scores stored in a SQLite database
- **Dynamic Visual Effects**: Enjoy particle effects, screen flashes, and color transitions
- **Educational Component**: Learn space facts after each game
- **Mobile-Friendly Design**: Optimized for various screen sizes and touch controls

## Technical Architecture

The game is built with a modular architecture:

- **`main.py`**: Entry point that initializes the game window
- **`ui.py`**: Contains the game screens, graphics rendering, and game logic
- **`leaderboard.py`**: Manages the SQLite database for player scores and space facts

### Visual Design

The game uses a blue-centric color palette designed to be visually appealing while avoiding red and yellow colors. All visual elements are created programmatically using Tkinter's canvas:

- Player ship is rendered as a green polygon
- Enemies are presented as distinct alien shapes with varying colors based on type
- Bullets, barriers, and effects use custom shapes and animations

## Requirements

- **Python 3.8+** (Python 3.10+ recommended)
- **Tkinter** (included with most Python installations)
- **SQLite3** (included with Python)
- **Additional packages**:
  - requests==2.31.0
  - Faker==19.12.0

## Installation Instructions

### Windows

1. **Install Python**:
   - Download Python from [python.org](https://www.python.org/downloads/windows/)
   - During installation, check "Add Python to PATH"
   - Ensure Tkinter is included (enabled by default)

2. **Clone the repository**:
   ```
   git clone https://github.com/yourusername/galacticdefendersv2.git
   cd galacticdefendersv2
   ```

3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

### macOS

1. **Install Python** (if not already installed):
   ```
   brew install python
   ```
   Or download from [python.org](https://www.python.org/downloads/macos/)

2. **Clone the repository**:
   ```
   git clone https://github.com/yourusername/galacticdefendersv2.git
   cd galacticdefendersv2
   ```

3. **Install dependencies**:
   ```
   pip3 install -r requirements.txt
   ```

### Linux

1. **Install Python and Tkinter**:
   ```
   sudo apt-get update
   sudo apt-get install python3 python3-pip python3-tk
   ```

2. **Clone the repository**:
   ```
   git clone https://github.com/yourusername/galacticdefendersv2.git
   cd galacticdefendersv2
   ```

3. **Install dependencies**:
   ```
   pip3 install -r requirements.txt
   ```

## Running the Game

Navigate to the game directory and run:

```
python main.py   # Windows
```

Or on macOS/Linux:

```
python3 main.py
```

## How to Play

1. **Start Screen**: Enter your name and press Enter or click "Start Game"
2. **Controls**:
   - **Arrow Keys/A,D**: Move ship left and right
   - **Spacebar**: Shoot
   - **P**: Pause/Resume game

3. **Game Mechanics**:
   - Defeat all aliens to advance to the next level
   - Each enemy type has different point values
   - Protect your ship with barriers (which degrade with damage)
   - Your ship has 3 shields (lives)
   - Game ends when you lose all shields or aliens reach the bottom

## Game Progression

The game increases in difficulty as you progress:
- Enemy movement speed increases
- Enemies shoot more frequently
- Enemies descend more quickly when hitting screen edges
- More enemy rows appear at higher levels
- Enemy bullet speed increases every 3 levels
- Bonus shield awarded every 10 levels

## Customization

You can modify game parameters by editing the following files:
- **`ui.py`**: Adjust game speed, enemy behavior, and visual effects
- **`leaderboard.py`**: Add or modify space facts

## Development

### Project Structure
```
galacticdefendersv2/
├── main.py              # Entry point
├── ui.py                # Game UI and logic
├── leaderboard.py       # Score management
├── requirements.txt     # Dependencies
├── README.md            # Documentation
└── gamedata.db          # SQLite database (created on first run)
```

### Contributing

1. Fork the repository
2. Create a feature branch:
   ```
   git checkout -b feature/your-feature-name
   ```
3. Implement your changes
4. Test thoroughly
5. Submit a pull request

## Troubleshooting

### Common Issues

1. **"No module named 'tkinter'"**:
   - Install Tkinter: `sudo apt-get install python3-tk` (Linux)

2. **Game runs slowly**:
   - Reduce the number of stars in the background
   - Modify the `ui.py` file to reduce particle effects

3. **Database errors**:
   - Ensure you have write permissions in the game directory

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

- **Developer**: Ilan Uzan
- **Inspiration**: Classic Space Invaders arcade game
- **Special Thanks**: To the Python and Tkinter communities
