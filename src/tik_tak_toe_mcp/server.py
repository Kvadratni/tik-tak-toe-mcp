import subprocess
import sys
import os
import json
from typing import Dict, List, Optional

from mcp.server.fastmcp import FastMCP
from mcp.shared.exceptions import McpError
from mcp.types import ErrorData, INTERNAL_ERROR, INVALID_PARAMS

mcp = FastMCP("tik-tak-toe")

# Path to save game state
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "game_state.json")

# Default game state
DEFAULT_GAME_STATE = {
    "board": [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]],
    "current_player": "X",
    "game_over": False,
    "winner": None,
    "ui_process": None,
    "agent_player": None  # The player symbol (X or O) that the agent controls
}

# Load game state from file or use default
def load_game_state():
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                state = json.load(f)
                # UI process can't be serialized, so we set it to None
                state["ui_process"] = None
                return state
        else:
            return DEFAULT_GAME_STATE.copy()
    except Exception as e:
        print(f"Error loading game state: {e}")
        return DEFAULT_GAME_STATE.copy()

# Save game state to file
def save_game_state(state):
    try:
        # Create a copy of the state without the UI process
        state_copy = state.copy()
        state_copy.pop("ui_process", None)
        
        with open(STATE_FILE, 'w') as f:
            json.dump(state_copy, f)
    except Exception as e:
        print(f"Error saving game state: {e}")

# Initialize game state
game_state = load_game_state()

@mcp.tool()
def start_game(agent_plays_as: str = "O") -> str:
    """
    Start a new Tic-Tac-Toe game and launch the UI.
    
    Args:
        agent_plays_as: Which player the agent will play as ("X" or "O")
    
    This will open a separate window with the game UI.
    """
    global game_state
    
    # Validate input
    if agent_plays_as not in ["X", "O"]:
        raise McpError(
            ErrorData(
                INVALID_PARAMS,
                f"Invalid player choice. Agent must play as 'X' or 'O'."
            )
        )
    
    # Reset the game state
    game_state = DEFAULT_GAME_STATE.copy()
    game_state["agent_player"] = agent_plays_as
    
    # Debug: Print the game state after initialization
    print(f"Game state after initialization: {json.dumps(game_state, default=str)}")
    
    # Save the game state
    save_game_state(game_state)
    
    # Launch the UI in a separate process
    try:
        # Kill any existing UI process
        if game_state["ui_process"] is not None:
            try:
                game_state["ui_process"].terminate()
            except:
                pass
        
        # Start a new UI process
        python_executable = sys.executable
        script_path = os.path.join(os.path.dirname(__file__), "ui", "__init__.py")
        game_state["ui_process"] = subprocess.Popen([python_executable, script_path])
        
        return f"New Tic-Tac-Toe game started! The UI should open in a separate window. You are playing as {agent_plays_as}, and the human plays as {'X' if agent_plays_as == 'O' else 'O'}."
    except Exception as e:
        raise McpError(
            ErrorData(
                INTERNAL_ERROR,
                f"Failed to start the UI: {str(e)}"
            )
        )

@mcp.tool()
def make_move(row: int, col: int) -> str:
    """
    Make a move on the Tic-Tac-Toe board.
    
    Args:
        row: Row index (0-2)
        col: Column index (0-2)
        
    Returns:
        A string describing the result of the move
    """
    global game_state
    
    # Reload game state to ensure we have the latest
    game_state = load_game_state()
    
    # Debug: Print the game state before the move
    print(f"Game state before move: {json.dumps(game_state, default=str)}")
    
    # Validate input
    if not (0 <= row <= 2 and 0 <= col <= 2):
        raise McpError(
            ErrorData(
                INVALID_PARAMS,
                f"Invalid position. Row and column must be between 0 and 2."
            )
        )
    
    # Check if the game is already over
    if game_state["game_over"]:
        return "Game is already over. Start a new game to play again."
    
    # Check if it's the agent's turn
    if game_state["current_player"] != game_state["agent_player"]:
        return f"It's not your turn. You are playing as {game_state['agent_player']}, but it's {game_state['current_player']}'s turn."
    
    # Check if the position is already occupied
    if game_state["board"][row][col] != " ":
        return f"Position ({row}, {col}) is already occupied. Try another position."
    
    # Make the move
    game_state["board"][row][col] = game_state["current_player"]
    
    # Debug: Print the game state after the move
    print(f"Game state after move: {json.dumps(game_state, default=str)}")
    
    # Check for a win
    winner = check_winner()
    if winner:
        game_state["game_over"] = True
        game_state["winner"] = winner
        save_game_state(game_state)
        return f"Player {winner} wins!"
    
    # Check for a draw
    if is_board_full():
        game_state["game_over"] = True
        save_game_state(game_state)
        return "It's a draw!"
    
    # Switch player
    game_state["current_player"] = "O" if game_state["current_player"] == "X" else "X"
    
    # Save the updated game state
    save_game_state(game_state)
    
    return f"Move made at ({row}, {col}). It's player {game_state['current_player']}'s turn."

@mcp.tool()
def get_board_state() -> str:
    """
    Get the current state of the Tic-Tac-Toe board.
    
    Returns:
        A string representation of the current board state
    """
    global game_state
    
    # Reload game state to ensure we have the latest
    game_state = load_game_state()
    
    # Debug: Print the current game state
    print(f"Current game state: {json.dumps(game_state, default=str)}")
    
    board_str = "\n"
    for i, row in enumerate(game_state["board"]):
        board_str += f" {row[0]} | {row[1]} | {row[2]} \n"
        if i < 2:
            board_str += "---+---+---\n"
    
    status = f"\nCurrent player: {game_state['current_player']}"
    
    # Add information about which player the agent is
    agent_info = f"\nYou are playing as: {game_state['agent_player']}"
    
    if game_state["game_over"]:
        if game_state["winner"]:
            status = f"\nGame over. Player {game_state['winner']} won!"
        else:
            status = "\nGame over. It's a draw!"
    elif game_state["current_player"] == game_state["agent_player"]:
        status += " (Your turn)"
    else:
        status += " (Human's turn)"
    
    return board_str + status + agent_info

def check_winner() -> Optional[str]:
    """Check if there's a winner and return the winning player."""
    board = game_state["board"]
    
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] != " ":
            return row[0]
    
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != " ":
            return board[0][col]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]
    
    return None

def is_board_full() -> bool:
    """Check if the board is full (draw condition)."""
    for row in game_state["board"]:
        if " " in row:
            return False
    return True

@mcp.resource(uri="mcp://tik-tak-toe/game_rules")
def game_rules() -> str:
    """
    Return the rules of Tic-Tac-Toe.
    """
    return """
    # Tic-Tac-Toe Rules
    
    1. The game is played on a 3x3 grid.
    2. Players take turns placing their mark (X or O) in an empty cell.
    3. The first player to get 3 of their marks in a row (horizontally, vertically, or diagonally) wins.
    4. If all cells are filled and no player has won, the game is a draw.
    
    ## How to Play with this MCP Extension
    
    1. Use `start_game(agent_plays_as="X")` or `start_game(agent_plays_as="O")` to begin a new game.
       - This determines which player you (the agent) will control.
       - The human player will control the other player.
    2. Use `make_move(row, col)` to place your mark at the specified position.
       - Rows and columns are indexed from 0 to 2.
       - You can only make moves when it's your turn.
    3. Use `get_board_state()` to see the current state of the board.
    """