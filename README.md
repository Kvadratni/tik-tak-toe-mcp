# Tic-Tac-Toe MCP Extension

A custom Model Context Protocol (MCP) extension for playing Tic-Tac-Toe with a separate UI.

## Features

- Play Tic-Tac-Toe through Goose AI
- Launches a separate UI window for the game
- Provides tools to start a game, make moves, and check the board state
- Includes game rules as a resource

## Installation

### Option 1: Install from PyPI

Install directly from PyPI using `uvx` (recommended):
```
uvx install tik-tak-toe-mcp
```

Or using pip:
```
pip install tik-tak-toe-mcp
```

### Option 2: Install from source

1. Clone this repository:
   ```
   git clone https://github.com/Kvadratni/tik-tak-toe-mcp.git
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

#### Option 1: Using uvx (recommended)

If you have installed Goose with `uvx`:

```
uvx goose --extension tik-tak-toe-mcp
```

#### Option 2: Manual setup

1. Go to Settings > Extensions > Add
2. Set Type to "StandardIO"
3. Provide ID, name, and description (e.g., "tik-tak-toe", "Tic-Tac-Toe Game", "Play Tic-Tac-Toe with a UI")
4. In the Command field, provide the path to the executable:
   ```
   tik-tak-toe-mcp
   ```

## Tools

- `start_game()`: Start a new Tic-Tac-Toe game and launch the UI
- `make_move(row, col)`: Make a move at the specified position (row and col are 0-2)
- `get_board_state()`: Get the current state of the board

## Resources

- `game_rules`: The rules of Tic-Tac-Toe and how to use this extension