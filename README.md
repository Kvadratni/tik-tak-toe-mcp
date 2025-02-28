# Tic-Tac-Toe MCP Extension

A custom Model Context Protocol (MCP) extension for playing Tic-Tac-Toe with a separate UI.

## Features

- Play Tic-Tac-Toe through Goose AI
- Launches a separate UI window for the game
- Provides tools to start a game, make moves, and check the board state
- Includes game rules as a resource

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/tik-tak-toe-mcp.git
   cd tik-tak-toe-mcp
   ```

2. Install the package:
   ```
   pip install -e .
   ```

## Usage

### As a standalone MCP server

Run the server:

```
tik-tak-toe-mcp
```

### With Goose

1. Go to Settings > Extensions > Add
2. Set Type to "StandardIO"
3. Provide ID, name, and description
4. In the Command field, provide the path to the executable:
   ```
   /path/to/python -m tik_tak_toe_mcp
   ```

## Tools

- `start_game()`: Start a new Tic-Tac-Toe game and launch the UI
- `make_move(row, col)`: Make a move at the specified position (row and col are 0-2)
- `get_board_state()`: Get the current state of the board

## Resources

- `game_rules`: The rules of Tic-Tac-Toe and how to use this extension