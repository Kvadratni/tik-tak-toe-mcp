import argparse
import logging
import sys
import os
from .server import mcp

# Set up logging to both console and file
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tik-tak-toe-mcp.log')
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

def main():
    """Tic-Tac-Toe MCP: Play Tic-Tac-Toe with a separate UI."""
    logging.info("Starting Tic-Tac-Toe MCP server...")
    try:
        parser = argparse.ArgumentParser(
            description="Play Tic-Tac-Toe with a separate UI."
        )
        parser.parse_args()
        logging.info("Running MCP server...")
        mcp.run()
    except Exception as e:
        logging.exception(f"Error running MCP server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()