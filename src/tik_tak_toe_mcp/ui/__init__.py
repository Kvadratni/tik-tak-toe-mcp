import tkinter as tk
from tkinter import messagebox
import os
import json
import time
import threading

# Path to save game state - same as in server.py
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "game_state.json")

class TicTacToeUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.geometry("300x400")
        
        # Load the initial game state
        self.load_game_state()
        
        # Create the game board UI
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(
                    root, 
                    text=self.board[i][j] if self.board[i][j] != " " else "", 
                    font=('Arial', 20), 
                    width=5, 
                    height=2,
                    command=lambda row=i, col=j: self.make_move(row, col)
                )
                button.grid(row=i, column=j, padx=5, pady=5)
                row.append(button)
            self.buttons.append(row)
        
        # Status label
        self.status_label = tk.Label(
            root, 
            text=self.get_status_text(), 
            font=('Arial', 12)
        )
        self.status_label.grid(row=3, column=0, columnspan=3, pady=10)
        
        # Player info label
        self.player_label = tk.Label(
            root, 
            text=self.get_player_info_text(),
            font=('Arial', 12)
        )
        self.player_label.grid(row=4, column=0, columnspan=3, pady=5)
        
        # Reset button
        self.reset_button = tk.Button(
            root, 
            text="New Game", 
            font=('Arial', 12),
            command=self.reset_game
        )
        self.reset_button.grid(row=5, column=0, columnspan=3, pady=5)
        
        # Start a thread to periodically check for updates
        self.should_update = True
        self.update_thread = threading.Thread(target=self.check_for_updates)
        self.update_thread.daemon = True
        self.update_thread.start()
        
        # Handle window close event
        root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def load_game_state(self):
        """Load the game state from the file shared with the server"""
        try:
            if os.path.exists(STATE_FILE):
                with open(STATE_FILE, 'r') as f:
                    state = json.load(f)
                    self.board = state["board"]
                    self.current_player = state["current_player"]
                    self.game_over = state["game_over"]
                    self.winner = state.get("winner", None)
                    self.agent_player = state.get("agent_player", None)
                    self.human_player = "O" if self.agent_player == "X" else "X" if self.agent_player else None
            else:
                # Default state if file doesn't exist
                self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
                self.current_player = "X"
                self.game_over = False
                self.winner = None
                self.agent_player = None
                self.human_player = None
        except Exception as e:
            print(f"Error loading game state: {e}")
            # Default state on error
            self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
            self.current_player = "X"
            self.game_over = False
            self.winner = None
            self.agent_player = None
            self.human_player = None
    
    def save_game_state(self):
        """Save the game state to the file shared with the server"""
        try:
            state = {
                "board": self.board,
                "current_player": self.current_player,
                "game_over": self.game_over,
                "winner": self.winner,
                "agent_player": self.agent_player
            }
            with open(STATE_FILE, 'w') as f:
                json.dump(state, f)
        except Exception as e:
            print(f"Error saving game state: {e}")
    
    def get_status_text(self):
        """Get the status text based on the current game state"""
        if self.game_over:
            if self.winner:
                return f"Game over. Player {self.winner} won!"
            else:
                return "Game over. It's a draw!"
        else:
            return f"Current player: {self.current_player}"
    
    def get_player_info_text(self):
        """Get text showing which player is human/agent"""
        if self.agent_player:
            return f"Human: {self.human_player} | Agent: {self.agent_player}"
        else:
            return "Player roles not set"
    
    def update_ui_from_state(self):
        """Update the UI to reflect the current game state"""
        # Update the buttons
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=self.board[i][j] if self.board[i][j] != " " else "")
        
        # Update the status label
        self.status_label.config(text=self.get_status_text())
        
        # Update the player info label
        self.player_label.config(text=self.get_player_info_text())
    
    def make_move(self, row, col):
        """Make a move on the board and update the UI"""
        if self.game_over or self.board[row][col] != " ":
            return
        
        # Check if it's the human's turn
        if self.agent_player and self.current_player != self.human_player:
            messagebox.showinfo("Not Your Turn", f"It's not your turn. You are playing as {self.human_player}.")
            return
        
        # Update the board and button
        self.board[row][col] = self.current_player
        self.buttons[row][col].config(text=self.current_player)
        
        # Check for a win
        winner = self.check_winner()
        if winner:
            self.game_over = True
            self.winner = winner
            self.status_label.config(text=f"Player {winner} wins!")
            messagebox.showinfo("Game Over", f"Player {winner} wins!")
            self.save_game_state()
            return
        
        # Check for a draw
        if self.is_board_full():
            self.game_over = True
            self.winner = None
            self.status_label.config(text="It's a draw!")
            messagebox.showinfo("Game Over", "It's a draw!")
            self.save_game_state()
            return
        
        # Switch player
        self.current_player = "O" if self.current_player == "X" else "X"
        self.status_label.config(text=f"Current player: {self.current_player}")
        
        # Save the updated game state
        self.save_game_state()
    
    def check_winner(self):
        """Check if there's a winner and return the winning player"""
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != " ":
                return row[0]
        
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != " ":
                return self.board[0][col]
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            return self.board[0][2]
        
        return None
    
    def is_board_full(self):
        """Check if the board is full (draw condition)"""
        for row in self.board:
            if " " in row:
                return False
        return True
    
    def reset_game(self):
        """Reset the game state and UI"""
        # Reset the board state but keep player assignments
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.current_player = "X"
        self.game_over = False
        self.winner = None
        
        # Reset the UI
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="")
        
        self.status_label.config(text=f"Current player: {self.current_player}")
        
        # Save the reset game state
        self.save_game_state()
    
    def check_for_updates(self):
        """Periodically check for updates to the game state file"""
        last_modified = 0
        if os.path.exists(STATE_FILE):
            last_modified = os.path.getmtime(STATE_FILE)
        
        while self.should_update:
            try:
                if os.path.exists(STATE_FILE):
                    current_modified = os.path.getmtime(STATE_FILE)
                    if current_modified > last_modified:
                        last_modified = current_modified
                        self.load_game_state()
                        self.root.after(0, self.update_ui_from_state)
            except Exception as e:
                print(f"Error checking for updates: {e}")
            
            time.sleep(0.5)  # Check every half second
    
    def on_close(self):
        """Handle window close event"""
        self.should_update = False
        self.root.destroy()

def main():
    root = tk.Tk()
    app = TicTacToeUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()