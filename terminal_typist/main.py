#!/usr/bin/env python3
"""
Terminal Typist - Main entry point
"""

import sys
import os
from .game import TypingGame

def main():
    """Main entry point for the terminal typing test"""
    try:
        game = TypingGame()
        game.run()
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for playing Terminal Typist!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
