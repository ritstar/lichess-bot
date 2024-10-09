# Chess Bot with Lichess API and Stockfish

This Python program allows you to play chess games on [Lichess](https://lichess.org/) in real-time, utilizing Stockfish as the engine for move suggestions. It displays the chess board visually and updates it in real-time, automatically playing moves on your behalf or offering suggestions based on your game's speed (Rapid/Blitz/Bullet).

## Features

- **Lichess Integration**: Fetches your current Lichess game and checks if it's your turn
- **Stockfish Integration**: Analyzes the current game state and provides the best move
- **Real-Time Board Updates**: Displays the chessboard and updates it after each move
- **Automated Moves**: Plays moves automatically if it's a Rapid game, otherwise suggests moves for Blitz/Bullet
- **Opponent Chat**: If the opponent is taking too long, the bot sends a polite chat message, "Play fast, please!"
- **Board Orientation**: Automatically adjusts the board orientation based on your color (white or black)
- **Checkmate Detection**: The program can detect if you've won, lost, or if the game has ended and exits gracefully

## Requirements

- Python 3.x
- [Stockfish](https://stockfishchess.org/) chess engine (ensure it's installed locally)
- Lichess API Key (get it [here](https://lichess.org/account/oauth/token))

## Dependencies

Install the required Python libraries:

```bash
pip install python-chess requests matplotlib cairosvg
```

## Setup

1. **Install Stockfish**:
   - Download and install the Stockfish engine from [here](https://stockfishchess.org/download/)
   - Ensure `stockfish` is available in your system's path or update the `STOCKFISH_PATH` in the script

2. **Get your Lichess API Key**:
   - Go to [Lichess API](https://lichess.org/account/oauth/token) and generate a personal API token
   - Copy the token and replace `your_lichess_api_key` in the script with your actual token

3. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/chess-bot.git
   cd chess-bot
   ```

4. **Update Constants**:
   - Open the Python script and update the `LICHESS_API_KEY` and `STOCKFISH_PATH` constants
   - Your Lichess API Key will be used to fetch the current game, and Stockfish is used for move analysis

   ```python
   STOCKFISH_PATH = "path_to_stockfish"  # Update with your local Stockfish path
   LICHESS_API_KEY = "your_lichess_api_key"  # Replace with your actual Lichess API key
   ```

## Running the Program

To run the chess bot, simply execute the Python script:

```bash
python lichess.py
```

The bot will:
- Fetch your current game
- Analyze the position
- Suggest or play moves (depending on game type)
- Update the board in real-time
- Send chat messages if the opponent is taking too long

## Known Issues

- **Blitz/Bullet Restrictions**: Lichess limits automated move-playing in Blitz/Bullet games, so the bot can only suggest moves for these games
- **Stockfish Path**: Ensure that Stockfish is correctly installed and accessible via the system path, or update the script with the correct path

## License

This project is licensed under the MIT License.