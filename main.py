#!/usr/bin/env python3
# Galactic Defenders - Main Entry Point
# Developed by Ilan Uzan

import tkinter as tk
from ui import SplashScreen

def main():
    """Main entry point for Galactic Defenders game."""
    # Create the root window
    root = tk.Tk()
    root.title("Galactic Defenders")
    root.resizable(False, False)
    
    # Set window size to match game canvas (800x600)
    root.geometry("800x600")
    
    # Start with the splash screen
    game = SplashScreen(root)
    
    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main() 