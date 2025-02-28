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

#### Option 1: Using Goose CLI (recommended)

Start Goose with your extension enabled:

```bash
# If you installed via PyPI
goose session --with-extension "tik-tak-toe-mcp"

# Or if you want to use a local development version
goose session --with-extension "python -m tik_tak_toe_mcp"
```

#### Option 2: Manual setup in Goose

1. Run `goose configure`
2. Select "Add Extension" from the menu
3. Choose "Command-line Extension"
4. Enter a name (e.g., "Tic-Tac-Toe Game")
5. For the command, enter: `tik-tak-toe-mcp`
6. Follow the prompts to complete the setup

## Tools

- `start_game()`: Start a new Tic-Tac-Toe game and launch the UI
- `make_move(row, col)`: Make a move at the specified position (row and col are 0-2)
- `get_board_state()`: Get the current state of the board

## Resources

- `game_rules`: The rules of Tic-Tac-Toe and how to use this extension