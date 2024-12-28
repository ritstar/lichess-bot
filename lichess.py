import requests
import time
import chess
import chess.engine
import chess.svg
import matplotlib.pyplot as plt
import cairosvg
import os
from dotenv import load_dotenv
import sys

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
    thinking_time = 0.2 if game_speed == 'blitz' or game_speed == 'bullet' else 0.3

    # Use Stockfish to analyze the position
    with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
        result = engine.play(board, chess.engine.Limit(time=thinking_time))
        best_move = result.move
        
        # You can add more sophisticated explanations here based on the analysis
        explanation = "Best move calculated based on evaluation."
        
        return best_move, explanation

# Check if the game has ended and print the result
def check_game_over(game_data):
    status = game_data.get('status', '')
    if status == 'mate':
        winner = "You" if game_data.get('winner') == game_data['color'] else "Your opponent"
        print("Game finished: Checkmate!")
        print(f"{winner} won the game.")
        return True
    elif status == 'resign':
        winner = "You" if game_data.get('winner') == game_data['color'] else "Your opponent"
        print("Game finished: Resignation!")
        print(f"{winner} won the game.")
        return True
    elif status == 'timeout':
        winner = "You" if game_data.get('winner') == game_data['color'] else "Your opponent"
        print("Game finished: Timeout!")
        print(f"{winner} won the game.")
        return True
    elif status == 'draw':
        print("Game finished: Draw!")
        return True
    return False

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
    cairosvg.svg2png(bytestring=board_svg, write_to="chess_board.png")  # Directly use bytestring, avoid creating files
    img = plt.imread("chess_board.png")
    
    plt.clf()  # Clear the previous plot
    plt.imshow(img)
    plt.axis('off')  # Turn off axis
    plt.pause(0.001)  # Pause briefly for real-time updates

def main():
    plt.ion()  # Turn on interactive mode for real-time board updates
    previous_fen = None  # Store the previous FEN to avoid redundant board updates
    move_count = 0  # Track the number of moves to detect slowdowns

    while True:
        fen, game_id, game_data = fetch_current_game()
        if fen and game_id:
            if check_game_over(game_data):  # Check if the game has ended
                print("Exiting program...")
                plt.close()  # Close the board display
                sys.exit()   # Exit the Python program

            if fen != previous_fen:  # Update the board only if the FEN has changed
                print(f"FEN: {fen}")
                previous_fen = fen
                move_count += 1  # Increment move counter
                
                # Determine whether to flip the board (if playing black)
                flip_board = game_data['color'] == 'black'

                # Visualize the board in real-time (no best move needed when not your turn)
                display_chess_board(fen, flip=flip_board)

                if game_data['isMyTurn']:
                    best_move, explanation = analyze_position(fen, game_data)
                    if best_move:
                        print(f"Suggested move: {best_move}")
                        print(f"Explanation: {explanation}")

                        # Visualize the board and highlight the move
                        display_chess_board(fen, best_move, flip=flip_board)

                        if game_data['speed'] == 'blitz' or game_data['speed'] == 'bullet':
                            print(f"{game_data['speed']} game detected. Please make the move manually.")
                        else:
                            play_move_on_lichess(game_id, best_move)
            else:
                print("Waiting for your turn...")
        
        # Check and mitigate performance slowdown
        if move_count % 10 == 0:
            plt.gcf().canvas.flush_events()  # Force a redraw to prevent lag
        
        # Update the board continuously regardless of the turn
        plt.pause(0.01)

if __name__ == "__main__":
    main()
