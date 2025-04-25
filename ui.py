#!/usr/bin/env python3
# Galactic Defenders - UI Module
# Handles UI, canvas, and game loop

import tkinter as tk
import random
import time
from functools import partial

class SplashScreen:
    def __init__(self, master):
        """Initialize the splash screen with ASCII art and rainbow effect."""
        self.master = master
        self.canvas = tk.Canvas(master, width=800, height=600, bg='black')
        self.canvas.pack(fill="both", expand=True)
        
        # Create starfield background
        self.create_starfield()
        
        # ASCII Art for the game title
        self.ascii_title = [
            "   _____       _            _   _          _____        __                _               ",
            "  / ____|     | |          | | (_)        |  __ \\      / _|              | |              ",
            " | |  __  __ _| | __ _  ___| |_ _  ___    | |  | | ___| |_ ___ _ __   __| | ___ _ __ ___ ",
            " | | |_ |/ _` | |/ _` |/ __| __| |/ __|   | |  | |/ _ \\  _/ _ \\ '_ \\ / _` |/ _ \\ '__/ __|",
            " | |__| | (_| | | (_| | (__| |_| | (__    | |__| |  __/ ||  __/ | | | (_| |  __/ |  \\__ \\",
            "  \\_____|\\__,_|_|\\__,_|\\___|\\__|_|\\___|   |_____/ \\___|_| \\___|_| |_|\\__,_|\\___|_|  |___/",
        ]
        
        # Display the ASCII title with rainbow colors
        self.title_elements = []
        self.display_ascii_title()
        
        # Add "Made by Ilan Uzan" text
        self.canvas.create_text(
            400, 350, 
            text="Made by Ilan Uzan", 
            fill="white", 
            font=("Courier", 16)
        )
        
        # Add "Press SPACE to start" text
        self.space_text = self.canvas.create_text(
            400, 450, 
            text="Press SPACE to start", 
            fill="white", 
            font=("Courier", 20, "bold")
        )
        
        # Bind space key to start the game
        self.master.bind("<space>", self.start_game)
        
        # Start animation loops
        self.blink_space_prompt()
        self.cycle_colors()
        
    def create_starfield(self):
        """Create a starfield background with stars of different sizes."""
        self.stars = []
        for _ in range(100):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            size = random.choice([1, 1, 1, 2, 2, 3])
            color = random.choice(['white', '#CCCCCC', '#999999', '#6666FF', '#9999FF'])
            star = self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline="")
            self.stars.append(star)
        
        # Create a few larger "distant galaxies"
        for _ in range(5):
            x = random.randint(50, 750)
            y = random.randint(50, 550)
            size = random.randint(3, 6)
            color = random.choice(['#6666FF', '#9966FF', '#CC66FF'])
            self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline="")
            
    def display_ascii_title(self):
        """Display the ASCII art title with initial white color."""
        y_pos = 120
        for line in self.ascii_title:
            text = self.canvas.create_text(
                400, y_pos, 
                text=line, 
                fill="white", 
                font=("Courier", 12)
            )
            self.title_elements.append(text)
            y_pos += 20
            
    def cycle_colors(self):
        """Cycle through rainbow colors for the ASCII title."""
        rainbow_colors = [
            "#FF0000", "#FF7F00", "#FFFF00", "#00FF00", 
            "#0000FF", "#4B0082", "#9400D3"
        ]
        
        color_index = 0
        for text_element in self.title_elements:
            self.canvas.itemconfig(text_element, fill=rainbow_colors[color_index % len(rainbow_colors)])
            color_index += 1
            
        # Schedule next color cycle
        self.master.after(150, self.cycle_colors)
            
    def blink_space_prompt(self):
        """Make the 'Press SPACE to start' text blink."""
        current_color = self.canvas.itemcget(self.space_text, "fill")
        new_color = "yellow" if current_color == "white" else "white"
        self.canvas.itemconfig(self.space_text, fill=new_color)
        self.master.after(500, self.blink_space_prompt)
        
    def start_game(self, event=None):
        """Transition from splash screen to player name entry."""
        # Clear canvas and remove splash screen elements
        self.canvas.delete("all")
        
        # Remove animation callbacks
        self.master.after_cancel(self.blink_space_prompt)
        self.master.after_cancel(self.cycle_colors)
        
        # Unbind space key
        self.master.unbind("<space>")
        
        # Create player name entry screen
        self.create_name_entry()
        
    def create_name_entry(self):
        """Create the player name entry screen."""
        # Recreate starfield background
        self.create_starfield()
        
        # Add prompt text
        self.canvas.create_text(
            400, 200, 
            text="Enter your name:", 
            fill="white", 
            font=("Courier", 24, "bold")
        )
        
        # Create entry field
        self.name_var = tk.StringVar()
        name_entry = tk.Entry(
            self.master, 
            textvariable=self.name_var,
            font=("Courier", 20),
            width=15,
            justify='center',
            bg='black',
            fg='#00FF00',  # Neon green
            insertbackground='#00FF00'  # Cursor color
        )
        
        # Place entry field on canvas
        self.name_entry_window = self.canvas.create_window(
            400, 250,
            window=name_entry
        )
        
        # Add submit button
        submit_button = tk.Button(
            self.master,
            text="Start Game",
            command=self.submit_name,
            font=("Courier", 16),
            bg='#333333',
            fg='#00FF00',
            activebackground='#555555',
            activeforeground='#FFFFFF',
            relief=tk.RAISED,
            bd=3
        )
        
        # Place button on canvas
        self.canvas.create_window(
            400, 320,
            window=submit_button
        )
        
        # Focus entry field
        name_entry.focus_set()
        
        # Bind Enter key to submit
        name_entry.bind("<Return>", self.submit_name)
        
    def submit_name(self, event=None):
        """Process the player name and start the game."""
        player_name = self.name_var.get().strip()
        
        # Validate name (3-15 alphanumeric chars)
        if not player_name.isalnum() or len(player_name) < 3 or len(player_name) > 15:
            # Show error message
            self.canvas.create_text(
                400, 380,
                text="Name must be 3-15 alphanumeric characters",
                fill="red",
                font=("Courier", 14)
            )
            self.master.after(2000, lambda: self.canvas.delete("error"))
            return
        
        # TODO: Start the actual game with the player's name
        print(f"Starting game for player: {player_name}")
        
        # For now, just show a placeholder message
        self.canvas.delete("all")
        self.canvas.create_text(
            400, 300,
            text=f"Welcome, {player_name}!\nGame implementation coming soon...",
            fill="white",
            font=("Courier", 20),
            justify="center"
        )

# This class will be implemented in future iterations
class GameScreen:
    def __init__(self, master, player_name):
        """Initialize the main game screen."""
        self.master = master
        self.player_name = player_name
        # TODO: Implement game mechanics 