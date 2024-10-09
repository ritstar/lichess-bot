import requests
import time
import chess
import chess.engine
import chess.svg
import matplotlib.pyplot as plt
import cairosvg
import os
from dotenv import load_dotenv

load_dotenv()

# Constants
STOCKFISH_PATH = "stockfish"  # Update with your local Stockfish path
LICHESS_API_KEY = os.getenv('lichess_api_key') #Your lichess API Key
WAIT_COUNT_LIMIT = 4  # Number of times to print 'Waiting for your turn...' before sending message

# Fetch current game state
def fetch_current_game():
    headers = {
        "Authorization": f"Bearer {LICHESS_API_KEY}"
    }
    response = requests.get("https://lichess.org/api/account/playing", headers=headers)
    data = response.json()

    if 'nowPlaying' in data and len(data['nowPlaying']) > 0:
        game = data['nowPlaying'][0]
        if game['isMyTurn']:
            return game['fen'], game['gameId'], game
    return None, None, None

# Play a move on Lichess
def play_move_on_lichess(game_id, move):
    headers = {
        "Authorization": f"Bearer {LICHESS_API_KEY}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    move_str = str(move)
    response = requests.post(f"https://lichess.org/api/board/game/{game_id}/move/{move_str}", headers=headers)
    if response.status_code == 200:
        print(f"Move {move_str} played successfully.")
    else:
        print(f"Error playing move on Lichess: {response.status_code}")
        print(response.json())

# Analyze the position with Stockfish and suggest a move
def analyze_position(fen, game_data):
    board = chess.Board(fen)
    
    # Set thinking time based on game type
    game_speed = game_data['speed']  # 'rapid' or 'blitz'
    thinking_time = 0.3 if game_speed == 'blitz' or game_speed == 'bullet' else 2.0

    # Use Stockfish to analyze the position
    with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
        result = engine.play(board, chess.engine.Limit(time=thinking_time))
        best_move = result.move
        
        # You can add more sophisticated explanations here based on the analysis
        explanation = "Best move calculated based on evaluation."
        
        return best_move, explanation

# Display the chess board using the given FEN and optional move highlight, oriented properly based on player's color
def display_chess_board(fen, move=None, flip=False):
    """
    Displays the chess board and updates it in real-time.
    :param fen: FEN string to represent the current board position.
    :param move: Optional move to highlight (chess.Move object).
    :param flip: Whether to flip the board (if you're playing black).
    """
    board = chess.Board(fen)
    
    # Generate the SVG of the board with the move highlighted and optional flip for black
    if move:
        board_svg = chess.svg.board(board, lastmove=move, size=400, orientation=chess.BLACK if flip else chess.WHITE)
    else:
        board_svg = chess.svg.board(board, size=400, orientation=chess.BLACK if flip else chess.WHITE)

    # Convert the SVG to PNG and display using matplotlib
    with open("chess_board.svg", "w") as f:
        f.write(board_svg)
    
    cairosvg.svg2png(url="chess_board.svg", write_to="chess_board.png")
    img = plt.imread("chess_board.png")
    plt.imshow(img)
    plt.axis('off')  # Turn off axis
    plt.pause(0.001)  # Pause briefly for real-time updates

def main():
    plt.ion()  # Turn on interactive mode for real-time board updates

    while True:
        fen, game_id, game_data = fetch_current_game()
        if fen and game_id:
            print(f"FEN: {fen}")
            best_move, explanation = analyze_position(fen, game_data)
            if best_move:
                print(f"Suggested move: {best_move}")
                print(f"Explanation: {explanation}")
                
                # Determine whether to flip the board (if playing black)
                flip_board = game_data['color'] == 'black'
                
                # Visualize the board and highlight the move in real-time
                display_chess_board(fen, best_move, flip=flip_board)
                
                # Check if it's a Blitz game
                if game_data['speed'] == 'blitz' or game_data['speed'] == 'bullet':
                    print(f"{game_data['speed']} game detected. Please make the move manually.")
                else:
                    play_move_on_lichess(game_id, best_move)
                    wait_count = 0  # Reset wait count after playing a move
            else:
                print("Could not analyze the position.")
            
        else:
            print("Waiting for your turn...")

        # Wait for 0.2 seconds before checking again, but update the board continuously
        time.sleep(0.2)

if __name__ == "__main__":
    main()