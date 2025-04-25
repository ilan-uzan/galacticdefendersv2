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
        
        # Remove any existing canvas
        for widget in master.winfo_children():
            widget.destroy()
            
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
        self.color_cycle_id = self.master.after(150, self.cycle_colors)
            
    def blink_space_prompt(self):
        """Make the 'Press SPACE to start' text blink."""
        current_color = self.canvas.itemcget(self.space_text, "fill")
        new_color = "yellow" if current_color == "white" else "white"
        self.canvas.itemconfig(self.space_text, fill=new_color)
        self.blink_id = self.master.after(500, self.blink_space_prompt)
        
    def start_game(self, event=None):
        """Transition from splash screen to player name entry."""
        # Clear canvas and remove splash screen elements
        self.canvas.delete("all")
        
        # Remove animation callbacks
        if hasattr(self, 'blink_id'):
            self.master.after_cancel(self.blink_id)
        if hasattr(self, 'color_cycle_id'):
            self.master.after_cancel(self.color_cycle_id)
        
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
        
        # Launch the game screen with the player's name
        self.launch_game_screen(player_name)
        
    def launch_game_screen(self, player_name):
        """Launch the main game screen with the player's name."""
        # Clean up the current screen
        self.canvas.delete("all")
        
        # Remove any existing bindings that might interfere
        self.master.unbind("<Return>")
        
        # Destroy any existing widgets
        for widget in self.canvas.winfo_children():
            widget.destroy()
            
        # Create the game screen
        game_screen = GameScreen(self.master, player_name)


class GameScreen:
    def __init__(self, master, player_name):
        """Initialize the main game screen."""
        self.master = master
        self.player_name = player_name
        
        # Clear existing widgets and bindings
        for widget in master.winfo_children():
            widget.destroy()
            
        # Unbind any existing key bindings
        for key in ['<space>', '<Left>', '<Right>', 'a', 'A', 'd', 'D', 'p', 'P']:
            self.master.unbind(key)
        
        # Game state variables
        self.score = 0
        self.shields = 3
        self.level = 1
        self.is_paused = False
        self.game_running = True
        
        # Player movement variables
        self.player_x = 400  # Initial x position centered
        self.player_speed = 7  # Speed of player movement
        self.player_width = 50  # Width of player ship
        self.key_states = {"left": False, "right": False}  # Track key states
        
        # Shooting variables
        self.bullets = []  # List to store bullet objects
        self.last_shot_time = 0  # Timestamp of the last shot fired
        self.bullet_cooldown = 300  # Cooldown in milliseconds (300ms = 0.3 seconds)
        self.bullet_speed = 10  # Pixels per frame
        
        # Create new canvas
        self.canvas = tk.Canvas(master, width=800, height=600, bg='black')
        self.canvas.pack(fill="both", expand=True)
        
        # Create the starfield background
        self.create_galaxy_background()
        
        # Initialize HUD (Heads-Up Display)
        self.initialize_hud()
        
        # Create player spaceship
        self.create_player_ship()
        
        # Add pause/play buttons
        self.create_pause_play_buttons()
        
        # Set up keyboard controls
        self.setup_controls()
        
        # Start the game loop
        self.update_game()
        
        # Debug info - print to console to confirm object creation
        print(f"Player ship created at x={self.player_x}")
        print(f"Game running state: {self.game_running}")
        
    def create_galaxy_background(self):
        """Create a galaxy-style starfield background."""
        # Draw a dark blue to purple gradient for space background
        for y in range(0, 600, 2):
            # Calculate color gradient from dark blue at top to purple at bottom
            r = int(10 + (y / 600) * 30)  # Dark blue to slightly less dark blue
            g = int(10 + (y / 600) * 10)  # Very little green
            b = int(40 + (y / 600) * 30)  # More blue/purple
            color = f'#{r:02x}{g:02x}{b:02x}'
            
            # Draw horizontal line with gradient color
            self.canvas.create_line(0, y, 800, y, fill=color)
        
        # Create stars of different sizes
        self.stars = []
        for _ in range(200):  # More stars for a richer background
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            size = random.choice([1, 1, 1, 2, 2, 3])
            color = random.choice(['white', '#CCCCCC', '#999999', '#6666FF', '#9999FF', '#DDDDFF'])
            star = self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline="")
            self.stars.append(star)
        
    def initialize_hud(self):
        """Initialize the Heads-Up Display (HUD)."""
        # Create HUD background - black bar at the top
        self.hud_bg = self.canvas.create_rectangle(
            0, 0, 800, 40, fill='#000000', outline=""
        )
        
        # Create score text
        self.score_text = self.canvas.create_text(
            100, 20, 
            text=f"Score: {self.score:04d}", 
            fill="#00FFFF",  # Cyan
            font=("Courier", 16, "bold")
        )
        
        # Create shields text
        self.shields_text = self.canvas.create_text(
            400, 20, 
            text=f"Shields: {self.shields}", 
            fill="#FF00FF",  # Magenta
            font=("Courier", 16, "bold")
        )
        
        # Create level text
        self.level_text = self.canvas.create_text(
            700, 20, 
            text=f"Level: {self.level}", 
            fill="#FFFF00",  # Yellow
            font=("Courier", 16, "bold")
        )
        
    def create_pause_play_buttons(self):
        """Create pause and play buttons."""
        # Create pause button frame
        pause_frame = tk.Frame(self.master, bg='black', bd=0, highlightthickness=0)
        pause_frame.place(x=750, y=45)
        
        # Create pause button
        self.pause_button = tk.Button(
            pause_frame,
            text="⏸️",  # Unicode pause symbol
            command=self.toggle_pause,
            font=("Arial", 12),
            bg='#333333',
            fg='#00FF00',
            activebackground='#555555',
            activeforeground='#FFFFFF',
            relief=tk.FLAT,
            bd=0,
            padx=2,
            pady=2
        )
        self.pause_button.pack()
        
        # Create play button (initially hidden)
        self.play_button = tk.Button(
            pause_frame,
            text="▶️",  # Unicode play symbol
            command=self.toggle_pause,
            font=("Arial", 12),
            bg='#333333',
            fg='#00FF00',
            activebackground='#555555',
            activeforeground='#FFFFFF',
            relief=tk.FLAT,
            bd=0,
            padx=2,
            pady=2
        )
        # Don't pack the play button yet, it will be shown when game is paused
        
        # Also bind 'p' key for pause/play
        self.master.bind('p', lambda event: self.toggle_pause())
        self.master.bind('P', lambda event: self.toggle_pause())
        
        # Ensure the buttons are visible by bringing the frame to the front
        pause_frame.lift()
        
    def toggle_pause(self):
        """Toggle the pause state of the game."""
        self.is_paused = not self.is_paused
        
        if self.is_paused:
            # Display "PAUSED" text
            self.pause_text = self.canvas.create_text(
                400, 300,
                text="PAUSED",
                fill="#FF0000",
                font=("Courier", 36, "bold")
            )
            # Switch buttons
            self.pause_button.pack_forget()
            self.play_button.pack()
        else:
            # Remove "PAUSED" text
            self.canvas.delete(self.pause_text)
            # Switch buttons
            self.play_button.pack_forget()
            self.pause_button.pack()
            
    def create_player_ship(self):
        """Create the player's spaceship."""
        # Ship coordinates - centered at bottom of screen
        ship_y = 550  # Position from top (near bottom of screen)
        
        # Create a sleek, modern spaceship using polygon
        # The design is inspired by classic arcade shooters but with a more refined look
        self.player = self.canvas.create_polygon(
            self.player_x, ship_y - 30,  # Top point
            self.player_x - 25, ship_y,  # Bottom left
            self.player_x - 15, ship_y - 10,  # Inner left
            self.player_x, ship_y - 15,  # Inner bottom
            self.player_x + 15, ship_y - 10,  # Inner right
            self.player_x + 25, ship_y,  # Bottom right
            fill="#00FFAA",  # Cyan-green
            outline="#FFFFFF",  # White outline
            width=1
        )
        
        # Check if object was created successfully
        if not self.player:
            print("WARNING: Failed to create player ship object!")
        else:
            print("Player ship object created successfully")
    
    def setup_controls(self):
        """Set up keyboard controls for the player ship."""
        # Bind key press events
        self.master.bind("<Left>", lambda event: self.set_key_state("left", True))
        self.master.bind("<Right>", lambda event: self.set_key_state("right", True))
        self.master.bind("a", lambda event: self.set_key_state("left", True))
        self.master.bind("A", lambda event: self.set_key_state("left", True))
        self.master.bind("d", lambda event: self.set_key_state("right", True))
        self.master.bind("D", lambda event: self.set_key_state("right", True))
        
        # Bind key release events
        self.master.bind("<KeyRelease-Left>", lambda event: self.set_key_state("left", False))
        self.master.bind("<KeyRelease-Right>", lambda event: self.set_key_state("right", False))
        self.master.bind("<KeyRelease-a>", lambda event: self.set_key_state("left", False))
        self.master.bind("<KeyRelease-A>", lambda event: self.set_key_state("left", False))
        self.master.bind("<KeyRelease-d>", lambda event: self.set_key_state("right", False))
        self.master.bind("<KeyRelease-D>", lambda event: self.set_key_state("right", False))
        
        # Bind space key for shooting
        self.master.bind("<space>", self.shoot)
    
    def set_key_state(self, key, is_pressed):
        """Update the state of a key (pressed or released)."""
        self.key_states[key] = is_pressed
    
    def update_player_position(self):
        """Update the player's position based on key states."""
        # Skip update if game is paused
        if self.is_paused:
            return
            
        # Calculate movement based on key states
        dx = 0
        if self.key_states["left"]:
            dx -= self.player_speed
        if self.key_states["right"]:
            dx += self.player_speed
            
        # Apply movement with screen boundary check
        new_x = self.player_x + dx
        
        # Screen boundaries with padding (half the ship width)
        if new_x - self.player_width/2 > 0 and new_x + self.player_width/2 < 800:
            self.player_x = new_x
            
            # Update ship position
            ship_coords = self.canvas.coords(self.player)
            
            # Translate all coordinates by dx
            for i in range(0, len(ship_coords), 2):
                ship_coords[i] += dx
                
            # Update ship polygon
            self.canvas.coords(self.player, *ship_coords)
    
    def update_game(self):
        """Update the game state and schedule the next update."""
        if self.game_running and not self.is_paused:
            # Update player position based on controls
            self.update_player_position()
            
            # Update bullet positions
            self.update_bullets()
            
            # Other game logic will go here in future implementations
            
        # Schedule the next update (approx. 60 FPS)
        self.game_update_id = self.master.after(16, self.update_game)
    
    def update_score(self, points):
        """Update the player's score."""
        self.score += points
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score:04d}")
    
    def update_shields(self, value):
        """Update the player's shields."""
        self.shields = max(0, self.shields + value)  # Prevent negative shields
        self.canvas.itemconfig(self.shields_text, text=f"Shields: {self.shields}")
        
        # Check for game over
        if self.shields <= 0 and self.game_running:
            self.game_over()
    
    def update_level(self, value=1):
        """Update the current level."""
        self.level += value
        self.canvas.itemconfig(self.level_text, text=f"Level: {self.level}")
    
    def shoot(self, event=None):
        """Create a bullet at the player's position."""
        # Return early if the game is paused or over
        if self.is_paused or not self.game_running:
            return
            
        # Check if enough time has passed since the last shot (cooldown)
        current_time = time.time() * 1000  # Convert to milliseconds
        if current_time - self.last_shot_time < self.bullet_cooldown:
            return  # Still on cooldown
        
        # Update the last shot timestamp
        self.last_shot_time = current_time
        
        # Get the current ship coordinates
        ship_coords = self.canvas.coords(self.player)
        
        # Calculate bullet starting position (top center of the ship)
        # The first point of the ship polygon is the top point (ship_coords[0], ship_coords[1])
        bullet_x = ship_coords[0]  # X-coordinate of the top of the ship
        bullet_y = ship_coords[1]  # Y-coordinate of the top of the ship
        
        # Create the bullet
        bullet = self.canvas.create_rectangle(
            bullet_x - 2, bullet_y - 10,
            bullet_x + 2, bullet_y,
            fill="#FF0000",  # Red color
            outline="#FF5555"  # Lighter red outline
        )
        
        # Add bullet to the tracking list
        self.bullets.append(bullet)
        
        # Optional: Add a small flash at the top of the ship
        flash = self.canvas.create_oval(
            bullet_x - 5, bullet_y - 5,
            bullet_x + 5, bullet_y + 5,
            fill="#FFFF00",  # Yellow flash
            outline=""
        )
        
        # Remove the flash after a short time
        self.master.after(50, lambda: self.canvas.delete(flash))
    
    def update_bullets(self):
        """Update the position of all bullets and remove those off screen."""
        bullets_to_remove = []
        
        for bullet in self.bullets:
            # Move bullet upward
            self.canvas.move(bullet, 0, -self.bullet_speed)
            
            # Get the current bullet position
            bullet_coords = self.canvas.coords(bullet)
            
            # Check if bullet is off screen (has moved beyond the top of the canvas)
            if bullet_coords and bullet_coords[3] < 0:
                bullets_to_remove.append(bullet)
        
        # Remove bullets that are off screen
        for bullet in bullets_to_remove:
            self.canvas.delete(bullet)
            self.bullets.remove(bullet)
    
    def game_over(self):
        """Handle game over state."""
        self.game_running = False
        
        # Cancel any scheduled animations/updates
        if hasattr(self, 'game_update_id'):
            self.master.after_cancel(self.game_update_id)
        
        # Clean up any remaining bullets
        for bullet in self.bullets:
            self.canvas.delete(bullet)
        self.bullets = []
        
        # Game over logic will be implemented in feature/game-over-screen branch 