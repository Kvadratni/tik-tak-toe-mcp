# Tic-Tac-Toe MCP Extension

A showcase example of building Model Context Protocol (MCP) servers with interactive UIs. This project demonstrates how to create an MCP extension that launches a separate UI window for playing Tic-Tac-Toe.

## Demo

Watch a demo of the Tic-Tac-Toe MCP Extension in action:



https://github.com/user-attachments/assets/a6ae4ba7-7a9c-42ed-bccc-56e6c988c266



[Direct link to video](https://github.com/Kvadratni/tik-tak-toe-mcp/raw/main/assets/tic-tac-toe-compressed.mp4)

## Features

- Demonstrates MCP server implementation with interactive UI components
- Showcases separation of AI interaction and user interface
- Play Tic-Tac-Toe through Goose AI with a separate visual interface
- Provides tools to start a game, make moves, and check the board state
- Includes game rules as a resource
- Serves as a template for building your own MCP extensions with UIs

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

#### Quick Install (One-Click)

Click the link below if you have Goose installed:

`goose://extension?cmd=uvx&arg=tik-tak-toe-mcp&id=tik_tak_toe&name=Tic-Tac-Toe%20Game&description=Play%20Tic-Tac-Toe%20with%20a%20separate%20UI`

#### Option 1: Using Goose CLI (recommended)

Start Goose with your extension enabled:

```bash
# If you installed via PyPI
goose session --with-extension "uvx tik-tak-toe-mcp"

# Or if you want to use a local development version
goose session --with-extension "python -m tik_tak_toe_mcp"
```

#### Option 2: Manual setup in Goose

1. Run `goose configure`
2. Select "Add Extension" from the menu
3. Choose "Command-line Extension"
4. Enter a name (e.g., "Tic-Tac-Toe Game")
5. For the command, enter: `uvx tik-tak-toe-mcp`
6. Follow the prompts to complete the setup

## Tools

- `start_game()`: Start a new Tic-Tac-Toe game and launch the UI
- `make_move(row, col)`: Make a move at the specified position (row and col are 0-2)
- `get_board_state()`: Get the current state of the board

## Resources

- `game_rules`: The rules of Tic-Tac-Toe and how to use this extension

## MCP Architecture Overview

This project showcases the Model Context Protocol (MCP) architecture for building AI-powered applications with separate UIs:

### Key Components

1. **MCP Server**: Handles communication between the AI model and the UI
   - Defines tools that the AI can use to interact with the game
   - Manages game state and logic
   - Provides a protocol for the UI to connect and receive updates

2. **Interactive UI**: A separate process that provides visual interaction
   - Renders the game board
   - Captures user input
   - Updates based on AI actions

3. **Integration with Goose AI**: 
   - The AI uses the provided tools to interact with the game
   - Tool calls are processed by the MCP server
   - Results are reflected in both the AI conversation and the UI

### Benefits Demonstrated

- **Separation of Concerns**: UI logic is separate from AI interaction
- **Enhanced User Experience**: Visual interface alongside AI conversation
- **Extensibility**: Pattern can be applied to more complex applications
- **Reusability**: Same MCP server can work with different AI models

This architecture can be adapted for various applications requiring both AI interaction and rich user interfaces.
