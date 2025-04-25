#!/usr/bin/env python3
# Galactic Defenders - UI Module
# Handles UI, canvas, and game loop

import tkinter as tk
import random
import time
from functools import partial
import math
from leaderboard import LeaderboardManager

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
            "#0088FF", "#00AAFF", "#00FFFF", 
            "#00FFAA", "#00FF00", "#0088AA",
            "#0066FF", "#6666FF", "#9966FF", "#CC66FF"
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
        self.width = 800
        self.height = 600
        
        # Initialize leaderboard manager
        self.leaderboard = LeaderboardManager()
        
        # Clear existing widgets and bindings
        for widget in master.winfo_children():
            widget.destroy()
            
        # Unbind any existing key bindings
        for key in ['<space>', '<Left>', '<Right>', 'a', 'A', 'd', 'D', 'p', 'P']:
            self.master.unbind(key)
        
        # Game state variables
        self.game_running = True
        self.is_paused = False
        self.score = 0
        self.level = 1
        self.shields = 3
        
        # Player related variables
        self.player_ship = None
        self.player_x = 400  # Start in middle of screen
        self.player_y = 550  # Near bottom of screen
        self.player_speed = 8  # Increased player speed for better control
        self.move_left = False
        self.move_right = False
        
        # Bullet related variables
        self.bullets = []
        self.last_shot_time = 0
        self.shot_cooldown = 250  # Faster shooting for player
        self.player_bullet_speed = 10  # Faster bullets
        
        # Enemy related variables
        self.enemies = []
        self.enemy_rows = 5
        self.enemy_cols = 10
        self.enemy_spacing_x = 60
        self.enemy_spacing_y = 50
        self.enemy_speed = 3  # Initial enemy speed (faster)
        self.enemy_direction = 1  # 1 for right, -1 for left
        self.enemy_move_timer = 0
        self.enemy_move_delay = 25  # Lower delay = faster movement
        self.enemy_descent_distance = 25  # Larger descent distance
        
        # Enemy bullets
        self.enemy_bullets = []
        self.enemy_bullet_speed = 6  # Faster enemy bullets
        self.enemy_shot_cooldown = 1000  # Shorter cooldown - shoot more often
        self.enemy_last_shot_time = 0
        self.max_enemy_bullets_onscreen = 8  # More enemy bullets at once
        
        # Particles list for special effects
        self.particles = []
        
        # Create new canvas
        self.canvas = tk.Canvas(master, width=800, height=600, bg='black')
        self.canvas.pack(fill="both", expand=True)
        
        # Create the starfield background
        self.create_galaxy_background()
        
        # Initialize HUD (Heads-Up Display)
        self.initialize_hud()
        
        # Update HUD with initial values
        self.update_hud()
        
        # Create player spaceship
        self.create_player_ship()
        
        # Create protective barriers
        self.create_barriers()
        
        # Spawn enemies
        self.spawn_enemies()
        
        # Add pause/play buttons
        self.create_pause_play_buttons()
        
        # Set up keyboard controls
        self.setup_controls()
        
        # Start the game loop
        self.update_game()
        
        # Debug info - print to console to confirm object creation
        print(f"Player ship created at x={self.player_x}")
        print(f"Game running state: {self.game_running}")
        print(f"Spawned {len(self.enemies)} enemies")
        
    def create_galaxy_background(self):
        """Create a galaxy-style starfield background."""
        # Create a solid black background without gradient lines
        self.canvas.configure(bg='black')
        
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
        """Initialize the heads-up display with score, level and shields."""
        # Create score display
        self.score_text = self.canvas.create_text(
            10, 10,  # Position: top-left
            text=f"Score: {self.score}",
            fill="#FFFFFF",
            font=("Courier", 14),
            anchor="nw"  # Northwest anchor to align at top-left
        )
        
        # Create level display
        self.level_text = self.canvas.create_text(
            400, 10,  # Position: top-center
            text=f"Level: {self.level}",
            fill="#FFFFFF",
            font=("Courier", 14),
            anchor="n"  # North anchor to align at top-center
        )
        
        # Create shields display
        self.shields_text = self.canvas.create_text(
            790, 10,  # Position: top-right
            text=f"Shields: {self.shields}",
            fill="#FFFFFF",
            font=("Courier", 14),
            anchor="ne"  # Northeast anchor to align at top-right
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
        
        # Clean up any unwanted items first
        self.clean_unwanted_items()
        
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
        self.player_ship = self.canvas.create_polygon(
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
        if not self.player_ship:
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
        if key == "left":
            self.move_left = is_pressed
        elif key == "right":
            self.move_right = is_pressed
    
    def update_player_position(self):
        """Update the player's position based on key states."""
        # Skip update if game is paused
        if self.is_paused:
            return
            
        # Calculate movement based on key states
        dx = 0
        if self.move_left:
            dx -= self.player_speed
        if self.move_right:
            dx += self.player_speed
            
        # Apply movement with screen boundary check
        new_x = self.player_x + dx
        
        # Screen boundaries with padding (half the ship width)
        if new_x - 25 > 0 and new_x + 25 < 800:
            self.player_x = new_x
            
            # Update ship position
            ship_coords = self.canvas.coords(self.player_ship)
            
            # Translate all coordinates by dx
            for i in range(0, len(ship_coords), 2):
                ship_coords[i] += dx
                
            # Update ship polygon
            self.canvas.coords(self.player_ship, *ship_coords)
    
    def update_game(self):
        """Update the game state and schedule the next update."""
        try:
            if self.game_running and not self.is_paused:
                # Clean up any stray dots or lines that might be showing
                self.clean_unwanted_items()
                
                # Update player position based on controls
                self.update_player_position()
                
                # Update bullet positions
                self.update_bullets()
                
                # Update enemy positions
                self.update_enemies()
                
                # Check for collisions
                self.check_collisions()
                
                # Handle enemy shooting
                self.enemy_shoot()
                
                # Update enemy bullets
                self.update_enemy_bullets()
                
                # Update special effects
                self._update_special_effects()
        except Exception as e:
            print(f"Error in game loop: {e}")
            
        # Schedule the next update (approx. 60 FPS)
        if hasattr(self, 'master') and self.master:
            self.master.after(16, self.update_game)
    
    def clean_unwanted_items(self):
        """Remove any stray dots or lines that might be visible."""
        # Find all items in the canvas
        all_items = self.canvas.find_all()
        
        for item_id in all_items:
            # Check item type
            item_type = self.canvas.type(item_id)
            item_tags = self.canvas.gettags(item_id)
            
            # Get position
            try:
                coords = self.canvas.coords(item_id)
            except:
                continue  # Skip if we can't get coordinates
                
            # Skip items we know should remain (like the player, barriers, etc.)
            if self.player_ship and item_id == self.player_ship:
                continue
                
            if 'barrier' in item_tags:
                continue
                
            # Check enemy bullets more safely
            enemy_bullet_ids = [b.get('id', -1) for b in self.enemy_bullets]
            if 'enemy_bullet' in item_tags or item_id in enemy_bullet_ids:
                continue
                
            if item_id in self.bullets:
                continue
                
            if item_id in self.stars:
                continue
                
            # Check for enemies more safely
            skip = False
            for enemy in self.enemies:
                if enemy.get('id', -1) == item_id:
                    skip = True
                    break
            if skip:
                continue
                
            # Check for HUD elements
            if hasattr(self, 'score_text') and item_id in [self.score_text, self.level_text, self.shields_text]:
                continue
                
            # Check if it's a tiny dot or line - this is safer
            if item_type in ['line', 'oval', 'rectangle']:
                try:
                    fill = self.canvas.itemcget(item_id, 'fill')
                    if fill in ['yellow', 'red'] or (isinstance(fill, str) and fill.startswith('#FF')):
                        self.canvas.delete(item_id)
                except Exception as e:
                    # Just skip items that cause errors
                    continue
    
    def update_score(self, points=10):
        """Update the player score."""
        self.score += points
        self.update_hud()
    
    def update_shields(self, value):
        """Update the player's shield value."""
        old_shields = self.shields
        self.shields = max(0, min(100, self.shields + value))
        
        # Flash screen blue if taking damage
        if value < 0:
            self.flash_screen("#6666FF")
            
        # Update the shields display
        self.update_hud()
        
        # If shields were depleted, end the game
        if old_shields > 0 and self.shields <= 0:
            self.game_over()
    
    def update_level(self, value=1):
        """Update the game level."""
        self.level += value
        self.update_hud()
        
        # Increase difficulty with level
        self.alien_speed = min(10, 1 + self.level * 0.5)
        self.alien_spawn_rate = max(1000, 5000 - self.level * 400)
    
    def shoot(self, event=None):
        """Create a bullet at the player's position."""
        # Return early if the game is paused or over
        if self.is_paused or not self.game_running or not self.player_ship:
            return
            
        # Check if enough time has passed since the last shot (cooldown)
        current_time = time.time() * 1000  # Convert to milliseconds
        if current_time - self.last_shot_time < self.shot_cooldown:
            return  # Still on cooldown
        
        # Update the last shot timestamp
        self.last_shot_time = current_time
        
        # Get the current ship coordinates
        try:
            ship_coords = self.canvas.coords(self.player_ship)
            if not ship_coords or len(ship_coords) < 2:
                return  # Invalid ship coordinates
        except:
            return  # Error getting ship coordinates
        
        # Calculate bullet starting position (top center of the ship)
        # The first point of the ship polygon is the top point (ship_coords[0], ship_coords[1])
        bullet_x = ship_coords[0]  # X-coordinate of the top of the ship
        bullet_y = ship_coords[1]  # Y-coordinate of the top of the ship
        
        # Create the bullet
        try:
            bullet = self.canvas.create_rectangle(
                bullet_x - 2, bullet_y - 10,
                bullet_x + 2, bullet_y,
                fill="#FF0000",  # Red color
                outline="#FF5555"  # Lighter red outline
            )
            
            # Add bullet to the tracking list
            self.bullets.append(bullet)
            
            # Play sound effect
            self.play_sound("player_shoot")
            
            # Optional: Add a small flash at the top of the ship
            flash = self.canvas.create_oval(
                bullet_x - 5, bullet_y - 5,
                bullet_x + 5, bullet_y + 5,
                fill="#FFFF00",  # Yellow flash
                outline=""
            )
            
            # Remove the flash after a short time
            self.master.after(50, lambda: self.canvas.delete(flash))
        except Exception as e:
            print(f"Error creating bullet: {e}")
    
    def update_bullets(self):
        """Update the position of all bullets and remove those off screen."""
        bullets_to_remove = []
        
        # Make a copy to avoid modifying during iteration
        for bullet in list(self.bullets):
            try:
                # Move bullet upward
                self.canvas.move(bullet, 0, -self.player_bullet_speed)
                
                # Get the current bullet position
                bullet_coords = self.canvas.coords(bullet)
                
                # Check if bullet is off screen (has moved beyond the top of the canvas)
                if not bullet_coords or bullet_coords[3] < 0:
                    bullets_to_remove.append(bullet)
                    continue
                    
                # Check for collision with barriers
                if self.check_bullet_hit_barrier(bullet_coords):
                    bullets_to_remove.append(bullet)
                    continue
            except:
                # If bullet no longer exists or causes error, remove it
                if bullet in self.bullets:
                    bullets_to_remove.append(bullet)
        
        # Remove bullets that are off screen or have hit barriers
        for bullet in bullets_to_remove:
            try:
                self.canvas.delete(bullet)
                if bullet in self.bullets:
                    self.bullets.remove(bullet)
            except:
                # Just continue if bullet was already removed
                pass
    
    def spawn_enemies(self):
        """Spawn the initial grid of enemies."""
        # Clear any existing enemies
        for enemy in self.enemies:
            self.canvas.delete(enemy["id"])
        self.enemies = []
        
        # Get enemy types
        enemy_types = self.get_enemy_types()
        
        # Start enemies from the top of the screen
        starting_y = 80
        
        for row in range(self.enemy_rows):
            enemy_type = enemy_types[row % len(enemy_types)]
            
            for col in range(self.enemy_cols):
                # Calculate position
                x = 100 + col * self.enemy_spacing_x
                y = starting_y + row * self.enemy_spacing_y
                
                # Create enemy based on its shape
                enemy_id = self.create_enemy(x, y, enemy_type)
                
                # Store enemy with its position data for tracking
                self.enemies.append({
                    "id": enemy_id,
                    "x": x,
                    "y": y,
                    "row": row,
                    "col": col,
                    "type": enemy_type["shape"],
                    "points": enemy_type["points"]
                })
    
    def create_enemy(self, x, y, enemy_type):
        """Create a Space Invaders style alien enemy."""
        size = enemy_type["size"]
        shape = enemy_type["shape"]
        fill = enemy_type["fill"]
        outline = enemy_type["outline"]
        
        # Base size for all aliens
        width = size * 2.5
        height = size * 2
        
        if shape == "alien1":  # Classic space invader with antennas
            # Create classic space invader shape
            enemy = self.canvas.create_polygon(
                # Left side
                x - width/2, y - height/4,
                x - width/3, y - height/4,
                x - width/3, y - height/2,
                x - width/6, y - height/2,
                x - width/6, y - height/4,
                x + width/6, y - height/4,
                # Right side
                x + width/6, y - height/2,
                x + width/3, y - height/2,
                x + width/3, y - height/4,
                x + width/2, y - height/4,
                # Bottom right
                x + width/2, y,
                x + width/3, y,
                x + width/3, y + height/4,
                x + width/6, y + height/4,
                # Bottom indent
                x + width/6, y,
                x - width/6, y,
                # Bottom left
                x - width/6, y + height/4,
                x - width/3, y + height/4,
                x - width/3, y,
                x - width/2, y,
                fill=fill,
                outline=outline,
                width=1
            )
            
        elif shape == "alien2":  # Crab-like alien
            enemy = self.canvas.create_polygon(
                # Top left antenna
                x - width/2, y - height/2,
                x - width/3, y - height/4,
                # Head top
                x - width/4, y - height/3,
                x + width/4, y - height/3,
                # Top right antenna
                x + width/3, y - height/4,
                x + width/2, y - height/2,
                # Right side
                x + width/2, y - height/3,
                x + width/3, y - height/6,
                x + width/2, y,
                x + width/3, y + height/6,
                # Bottom feelers
                x + width/4, y + height/3,
                x, y + height/4,
                x - width/4, y + height/3,
                # Left side
                x - width/3, y + height/6,
                x - width/2, y,
                x - width/3, y - height/6,
                x - width/2, y - height/3,
                fill=fill,
                outline=outline,
                width=1
            )
            
        elif shape == "alien3":  # Squid-like alien
            enemy = self.canvas.create_polygon(
                # Head
                x, y - height/2,
                # Right head side
                x + width/6, y - height/3,
                x + width/3, y - height/4,
                # Right arms
                x + width/2, y - height/6,
                x + width/3, y,
                x + width/4, y + height/6,
                # Tentacles
                x + width/3, y + height/3,
                x + width/6, y + height/2,
                x, y + height/3,
                x - width/6, y + height/2,
                x - width/3, y + height/3,
                # Left arms
                x - width/4, y + height/6,
                x - width/3, y,
                x - width/2, y - height/6,
                # Left head side
                x - width/3, y - height/4,
                x - width/6, y - height/3,
                fill=fill,
                outline=outline,
                width=1
            )
            
        elif shape == "alien4":  # Boss alien
            # Create main body
            enemy = self.canvas.create_polygon(
                # Top of head
                x - width/3, y - height/2,
                x + width/3, y - height/2,
                # Right side
                x + width/2, y - height/3,
                x + width/3, y,
                # Bottom appendages
                x + width/2, y + height/4,
                x + width/4, y + height/2,
                x, y + height/3,
                x - width/4, y + height/2,
                x - width/2, y + height/4,
                # Left side
                x - width/3, y,
                x - width/2, y - height/3,
                fill=fill,
                outline=outline,
                width=1
            )
            # Add eyes
            self.canvas.create_oval(
                x - width/6, y - height/4,
                x - width/12, y - height/6,
                fill="#FFFFFF",
                outline=outline
            )
            self.canvas.create_oval(
                x + width/12, y - height/4,
                x + width/6, y - height/6,
                fill="#FFFFFF",
                outline=outline
            )
            
        elif shape == "alien5":  # UFO mothership - simplified without lights
            # Create oval for UFO body
            enemy = self.canvas.create_oval(
                x - width/1.5, y - height/3,
                x + width/1.5, y + height/3,
                fill=fill,
                outline=outline,
                width=1
            )
            # Add a small ridge on top for detail without cockpit
            self.canvas.create_rectangle(
                x - width/4, y - height/3 - 2,
                x + width/4, y - height/3,
                fill=fill,
                outline=outline
            )
        else:
            # Default to a simple rectangular alien if shape not recognized
            enemy = self.canvas.create_rectangle(
                x - width/2, y - height/2,
                x + width/2, y + height/2,
                fill=fill,
                outline=outline,
                width=1
            )
            
        return enemy
    
    def update_enemies(self):
        """Update the enemy positions using Space Invaders style movement."""
        # Skip if no enemies or paused
        if not self.enemies or self.is_paused:
            return
            
        # Increment timer, only move enemies on certain frames
        self.enemy_move_timer += 1
        if self.enemy_move_timer < self.enemy_move_delay:
            return
        
        # Reset the timer
        self.enemy_move_timer = 0
        
        # Check if any enemies have reached the edges
        try:
            leftmost_x = min(enemy["x"] for enemy in self.enemies if enemy.get("x") is not None)
            rightmost_x = max(enemy["x"] for enemy in self.enemies if enemy.get("x") is not None)
            lowest_y = max(enemy["y"] for enemy in self.enemies if enemy.get("y") is not None)
        except ValueError:
            # No valid enemies with coordinates found
            return
        
        # Check for edge collision and game over
        hit_edge = False
        if (self.enemy_direction > 0 and rightmost_x + 20 >= 800) or \
           (self.enemy_direction < 0 and leftmost_x - 20 <= 0):
            hit_edge = True
        
        # Check if enemies are getting too close to player - game over
        if lowest_y >= self.player_y - 50:
            self.game_over(invasion=True)
            return
        
        # If hit edge, change direction and move down
        if hit_edge:
            self.enemy_direction *= -1
            
            # Move all enemies down
            enemies_to_update = list(self.enemies)  # Make a copy for safe iteration
            for enemy in enemies_to_update:
                try:
                    if "y" in enemy and "id" in enemy:
                        enemy["y"] += self.enemy_descent_distance
                        self.canvas.move(enemy["id"], 0, self.enemy_descent_distance)
                except Exception as e:
                    # If enemy causes error, just skip it
                    continue
                
            # Play sound
            self.play_sound("enemy_descend")
                
            # Increase enemy speed slightly after each descent
            self.enemy_move_delay = max(5, self.enemy_move_delay - 1)
        else:
            # Move horizontally in current direction
            dx = self.enemy_speed * self.enemy_direction
            enemies_to_update = list(self.enemies)  # Make a copy for safe iteration
            for enemy in enemies_to_update:
                try:
                    if "x" in enemy and "id" in enemy:
                        enemy["x"] += dx
                        self.canvas.move(enemy["id"], dx, 0)
                except Exception as e:
                    # If enemy causes error, just skip it
                    continue
        
        # Animate aliens (toggle between shapes for a classic Space Invaders effect)
        enemies_to_animate = list(self.enemies)  # Make a copy for safe iteration
        for enemy in enemies_to_animate:
            try:
                # Get current outline color
                outline_color = self.canvas.itemcget(enemy["id"], "outline")
                
                # Toggle between normal and brighter outline
                if "88" in outline_color:  # If it's already bright
                    new_color = outline_color.replace("88", "FF")
                else:  # If it's dim
                    new_color = outline_color.replace("FF", "88")
                    
                self.canvas.itemconfig(enemy["id"], outline=new_color)
            except Exception as e:
                # If enemy causes error, just skip it
                continue
    
    def check_collisions(self):
        """Check for collisions between bullets and enemies."""
        # Create a copy of bullets and enemies since we'll be removing items during iteration
        bullets_to_check = list(self.bullets)
        enemies_to_check = list(self.enemies)
        
        for bullet in bullets_to_check:
            if bullet not in self.bullets:  # Skip if bullet was already removed
                continue
                
            # Get bullet position
            try:
                bullet_coords = self.canvas.coords(bullet)
                if not bullet_coords:  # Skip if bullet was deleted
                    continue
                    
                # Calculate bullet center
                bullet_x = (bullet_coords[0] + bullet_coords[2]) / 2
                bullet_y = (bullet_coords[1] + bullet_coords[3]) / 2
                
                for enemy in enemies_to_check:
                    if enemy not in self.enemies:  # Skip if enemy was already removed
                        continue
                        
                    # Get enemy bounding box
                    enemy_coords = self.canvas.bbox(enemy["id"])
                    if not enemy_coords:  # Skip if enemy was deleted
                        continue
                    
                    # Check if bullet is inside enemy bounding box
                    if (bullet_x >= enemy_coords[0] and bullet_x <= enemy_coords[2] and
                        bullet_y >= enemy_coords[1] and bullet_y <= enemy_coords[3]):
                        # Collision occurred!
                        self.handle_enemy_hit(enemy, bullet)
                        # Break since this bullet has hit something
                        break
            except Exception as e:
                # Skip problematic bullets
                print(f"Error in collision detection: {e}")
                continue
    
    def handle_enemy_hit(self, enemy, bullet):
        """Handle what happens when an enemy is hit by a bullet."""
        # No explosion effect as requested by user
        
        # Increment score based on enemy type
        points = enemy["points"]
        
        # Update score
        self.score += points
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
        
        # Remove enemy from canvas and list
        self.canvas.delete(enemy["id"])
        self.enemies.remove(enemy)
        
        # Remove bullet from canvas and list
        self.canvas.delete(bullet)
        if bullet in self.bullets:
            self.bullets.remove(bullet)
            
        # Check if all enemies are defeated
        if not self.enemies:
            self.level_complete()
    
    def create_explosion(self, x, y):
        """Create a visual explosion effect."""
        # Create multiple explosion particles
        particles = []
        # Use only white/blue colors to avoid red/yellow
        colors = ["#FFFFFF", "#CCCCFF", "#8888FF", "#6666FF"]  # White to blue colors
        
        # Create 8 particles in different directions
        for i in range(8):
            angle = math.radians(i * 45)  # 8 directions (0, 45, 90, 135, etc.)
            dx = math.cos(angle) * 5
            dy = math.sin(angle) * 5
            color = random.choice(colors)
            
            # Create small circle for particle
            particle = self.canvas.create_oval(
                x - 3, y - 3, 
                x + 3, y + 3, 
                fill=color, outline=""
            )
            
            particles.append({"id": particle, "dx": dx, "dy": dy, "life": 10})
        
        # Animate the explosion
        self.animate_explosion(particles)
    
    def animate_explosion(self, particles, frame=0):
        """Animate the explosion particles."""
        still_alive = False
        
        for p in particles:
            if p["life"] > 0:
                # Move particle
                self.canvas.move(p["id"], p["dx"], p["dy"])
                
                # Fade particle (reduce opacity)
                p["life"] -= 1
                opacity = int(p["life"] * 25.5)  # 255 * (life/10)
                color = self.canvas.itemcget(p["id"], "fill")
                
                # Reduce size slightly
                coords = self.canvas.coords(p["id"])
                new_coords = [
                    coords[0] + 0.2, coords[1] + 0.2,
                    coords[2] - 0.2, coords[3] - 0.2
                ]
                self.canvas.coords(p["id"], *new_coords)
                
                still_alive = True
            else:
                # Remove dead particles
                self.canvas.delete(p["id"])
        
        # Continue animation if particles still exist
        if still_alive and frame < 10 and self.game_running:
            self.master.after(20, lambda: self.animate_explosion(particles, frame + 1))
    
    def level_complete(self):
        """Handle level completion."""
        # Increment level
        self.level += 1
        
        # Update level display
        self.canvas.itemconfig(self.level_text, text=f"Level: {self.level}")
        
        # Display level completion message
        level_msg = self.canvas.create_text(
            400, 300,  # Center of screen
            text=f"LEVEL {self.level-1} COMPLETE!",
            font=("Courier", 30, "bold"),
            fill="#00FF00",
            tags="level_msg"
        )
        
        # Show next level message
        next_msg = self.canvas.create_text(
            400, 350,
            text=f"PREPARE FOR LEVEL {self.level}",
            font=("Courier", 20),
            fill="#FFFFFF",
            tags="level_msg"
        )
        
        # Schedule removal of message and spawn of new enemies
        self.master.after(3000, self.clear_level_message)
        self.master.after(3500, self.spawn_new_level)
    
    def clear_level_message(self):
        """Clear the level completion message."""
        self.canvas.delete("level_msg")
    
    def spawn_new_level(self):
        """Spawn enemies for the new level with increased difficulty."""
        # Increase difficulty with level - more aggressive aliens in higher levels
        self.enemy_speed = min(2 + self.level * 0.6, 10)  # Faster movement in higher levels (up to 10)
        self.enemy_move_delay = max(30 - self.level * 3, 3)  # Much quicker movement at higher levels
        
        # Increase enemy bullets as levels progress
        self.max_enemy_bullets_onscreen = min(5 + self.level, 20)  # More bullets at once
        
        # Decrease enemy shot cooldown (much more frequent shots at higher levels)
        self.enemy_shot_cooldown = max(1000 - (self.level * 60), 200)  # Down to 200ms cooldown
        
        # Add more enemy rows every 2 levels (up to 7)
        self.enemy_rows = min(4 + (self.level - 1) // 2, 7)
        
        # Every 3 levels, increase enemy bullet speed
        if self.level % 3 == 0:
            self.enemy_bullet_speed += 1
        
        # Award bonus shield every 10 levels
        if self.level % 10 == 0:
            self.shields += 1
            self.update_hud()
            # Show bonus life message
            bonus_msg = self.canvas.create_text(
                400, 350,
                text="BONUS SHIELD AWARDED!",
                fill="#00FF00",
                font=("Courier", 20, "bold"),
                tags="level_msg"
            )
            self.master.after(2000, lambda: self.canvas.delete(bonus_msg))
        
        # Clear and regenerate barriers
        self.regenerate_barriers()
        
        # Spawn the enemies
        self.spawn_enemies()
        
        # Display level message with difficulty indicator
        level_difficulty = "EXTREME" if self.level > 15 else "HARD" if self.level > 10 else "MEDIUM" if self.level > 5 else "NORMAL"
        level_msg = self.canvas.create_text(
            400, 300,
            text=f"LEVEL {self.level} - {level_difficulty} DIFFICULTY",
            fill="#FFFFFF",
            font=("Courier", 18, "bold"),
            tags="level_msg"
        )
        self.master.after(2000, lambda: self.canvas.delete(level_msg))
    
    def regenerate_barriers(self):
        """Clear and recreate the protective barriers."""
        # Remove existing barriers
        for block in self.barrier_blocks:
            self.canvas.delete(block["id"])
        
        self.barriers = []
        self.barrier_blocks = []
        
        # Create new barriers
        self.create_barriers()
    
    def game_over(self, invasion=False):
        """Handle game over state."""
        # Set game running to false
        self.game_running = False
        
        # Save score to leaderboard
        self.leaderboard.add_score(self.player_name, self.score, self.level)
        
        # Get player rank
        player_rank = self.leaderboard.get_player_rank(self.player_name, self.score)
        
        # Get a random space fact
        space_fact = self.leaderboard.get_random_space_fact()
        
        # Get top 5 scores
        top_scores = self.leaderboard.get_top_scores(5)
        
        # Cancel any scheduled animations/updates
        if hasattr(self, 'game_update_id'):
            self.master.after_cancel(self.game_update_id)
        
        # Start with a fresh canvas to avoid any issues
        self.canvas.delete("all")
        
        # Recreate the galaxy background for the game over screen
        self.create_galaxy_background()
        
        # Reset data structures
        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []
        
        # Different message based on how game ended
        game_over_msg = "GAME OVER"
        if invasion:
            game_over_msg = "EARTH INVADED!"
        
        # Show game over message with blue instead of red
        self.canvas.create_text(
            400, 150,
            text=game_over_msg,
            fill="#6666FF",  # Blue text instead of red
            font=("Courier", 36, "bold")
        )
        
        # Show player score
        self.canvas.create_text(
            400, 200,
            text=f"Final Score: {self.score}",
            fill="#FFFFFF",
            font=("Courier", 24)
        )
        
        # Show player rank
        self.canvas.create_text(
            400, 230,
            text=f"Rank: #{player_rank}",
            fill="#00FFAA",
            font=("Courier", 18)
        )
        
        # Show space fact header
        self.canvas.create_text(
            400, 270,
            text="SPACE FACT:",
            fill="#00FFFF",
            font=("Courier", 14, "bold")
        )
        
        # Show space fact
        fact_text = self.canvas.create_text(
            400, 295,
            text=space_fact,
            fill="#CCCCFF",
            font=("Courier", 12),
            width=600,  # Wrap text if needed
            justify=tk.CENTER
        )
        
        # Draw a separator line
        self.canvas.create_line(200, 320, 600, 320, fill="#444444", width=2)
        
        # Leaderboard title
        self.canvas.create_text(
            400, 340,
            text="TOP SCORES",
            fill="#00FF88",
            font=("Courier", 16, "bold")
        )
        
        # Display leaderboard entries
        y_pos = 370
        for i, (name, score, level, date) in enumerate(top_scores):
            # Highlight the current player's score
            is_player = name == self.player_name and score == self.score
            color = "#FFFF00" if is_player else "#FFFFFF"
            
            # Format the leaderboard entry
            entry_text = f"{i+1}. {name}: {score} pts (Level {level})"
            
            self.canvas.create_text(
                400, y_pos,
                text=entry_text,
                fill=color,
                font=("Courier", 14)
            )
            y_pos += 25
        
        # Play again prompt
        self.canvas.create_text(
            400, 550,
            text="Press SPACE to play again",
            fill="#00FF00",
            font=("Courier", 16)
        )
        
        # Make sure the spaceship and barriers don't remain
        self.player_ship = None
        self.barrier_blocks = []
        
        # Bind space to restart with a more reliable approach
        self.master.bind("<space>", self.restart_game_safe)
        
    def restart_game_safe(self, event=None):
        """A safer version of restart_game to avoid freezing."""
        try:
            # Try to completely reset the game UI
            self.canvas.delete("all")
            
            # Store the player name and leaderboard for reuse
            player_name = self.player_name
            leaderboard = self.leaderboard
            
            # Reset game state
            self.game_running = True
            self.is_paused = False
            self.score = 0
            self.level = 1
            self.shields = 3
            
            # Reset player position
            self.player_x = 400
            self.player_y = 550
            
            # Reset movement flags
            self.move_left = False
            self.move_right = False
            
            # Reset all game elements
            self.bullets = []
            self.enemy_bullets = []
            self.enemies = []
            self.enemy_speed = 3
            self.enemy_direction = 1
            self.enemy_move_timer = 0
            self.enemy_move_delay = 25
            self.stars = []
            self.barriers = []
            self.barrier_blocks = []
            
            # Restore player name and leaderboard
            self.player_name = player_name
            self.leaderboard = leaderboard
            
            # Recreate the game elements
            self.create_galaxy_background()
            self.initialize_hud()
            self.update_hud()
            self.create_player_ship()
            self.create_barriers()
            self.spawn_enemies()
            self.create_pause_play_buttons()
            
            # Set up controls again
            self.setup_controls()
            
            # Start the game loop
            self.update_game()
            
        except Exception as e:
            # Fallback if anything goes wrong
            print(f"Error during restart: {e}")
            # Create a new game screen as a last resort
            self.master.after(100, lambda: GameScreen(self.master, self.player_name))
    
    def enemy_shoot(self):
        """Randomly select enemies to shoot."""
        # Don't shoot if game is paused or over
        if not self.game_running or self.is_paused:
            return
        
        # Maximum of 5 enemy bullets at once
        if len(self.enemy_bullets) >= 5:
            return
        
        # Chance of shooting increases as enemies get closer to the player
        if not self.enemies:
            return
            
        # Find the lowest enemy in each column
        enemy_columns = {}
        for enemy in self.enemies:
            try:
                if 'id' not in enemy:
                    continue
                    
                coords = self.canvas.coords(enemy['id'])
                if not coords:
                    continue
                    
                x1, y1, x2, y2 = 0, 0, 0, 0
                if len(coords) >= 4:  # Rectangle or oval
                    x1, y1, x2, y2 = coords[0], coords[1], coords[2], coords[3]
                else:  # Polygon - use bounding box
                    bbox = self.canvas.bbox(enemy['id'])
                    if bbox:
                        x1, y1, x2, y2 = bbox
                
                center_x = (x1 + x2) / 2
                column = int(center_x / 50)  # Group into columns
                
                if column not in enemy_columns or y2 > self.canvas.coords(enemy_columns[column]['id'])[3]:
                    enemy_columns[column] = enemy
            except Exception as e:
                continue
                
        # Randomly select columns to shoot from
        for enemy in enemy_columns.values():
            if random.random() < 0.02:  # 2% chance per column per frame
                try:
                    coords = self.canvas.coords(enemy['id'])
                    if not coords:
                        continue
                        
                    x1, y1, x2, y2 = 0, 0, 0, 0
                    if len(coords) >= 4:  # Rectangle or oval
                        x1, y1, x2, y2 = coords[0], coords[1], coords[2], coords[3]
                    else:  # Polygon - use bounding box
                        bbox = self.canvas.bbox(enemy['id'])
                        if bbox:
                            x1, y1, x2, y2 = bbox
                    
                    center_x = (x1 + x2) / 2
                    center_y = y2
                    
                    # Create the enemy bullet
                    self.create_enemy_bullet(center_x, center_y)
                except Exception as e:
                    continue
    
    def update_enemy_bullets(self):
        """Update positions of enemy bullets."""
        bullets_to_remove = []
        
        # Use a copy of the list for safer iteration
        for bullet in list(self.enemy_bullets):
            try:
                # Move bullet with its velocity components
                self.canvas.move(bullet["id"], bullet["dx"], bullet["dy"])
                
                # Get bullet position
                bullet_coords = self.canvas.coords(bullet["id"])
                
                # Check if bullet has gone off screen
                if not bullet_coords or bullet_coords[1] > 600 or bullet_coords[0] < 0 or bullet_coords[2] > 800:
                    bullets_to_remove.append(bullet)
                    continue
                    
                # Check for collision with barriers
                if self.check_bullet_hit_barrier(bullet_coords):
                    bullets_to_remove.append(bullet)
                    continue
                    
                # Check for collision with player
                if self.check_bullet_hit_player(bullet_coords):
                    bullets_to_remove.append(bullet)
            except:
                # If bullet causes error, remove it
                bullets_to_remove.append(bullet)
                
        # Remove bullets
        for bullet in bullets_to_remove:
            try:
                if bullet in self.enemy_bullets:
                    self.enemy_bullets.remove(bullet)
                self.canvas.delete(bullet["id"])
            except:
                # Just continue if already removed
                pass
    
    def check_bullet_hit_player(self, bullet_coords):
        """Check if an enemy bullet hit the player."""
        # Skip if player does not exist
        if not self.player_ship:
            return False
            
        # Get player bounds
        player_coords = self.canvas.bbox(self.player_ship)
        if not player_coords:
            return False
            
        # Calculate bullet center
        bullet_x = (bullet_coords[0] + bullet_coords[2]) / 2
        bullet_y = (bullet_coords[1] + bullet_coords[3]) / 2
        
        # Check if bullet is inside player bounding box
        if (bullet_x >= player_coords[0] and bullet_x <= player_coords[2] and
            bullet_y >= player_coords[1] and bullet_y <= player_coords[3]):
            # Player is hit!
            self.player_hit()
            return True
        
        return False
    
    def player_hit(self):
        """Handle player being hit by enemy bullet."""
        # Skip if player is already flashing (invulnerable)
        if hasattr(self, 'is_flashing') and self.is_flashing:
            return
            
        # Flash screen blue if taking damage (was red)
        self.flash_screen("#6666FF")
        
        # Decrease shields
        self.shields -= 1
        
        # Update shields display
        self.update_hud()
        
        # Visual feedback
        self.flash_player()
        
        # Check if game over
        if self.shields < 0:
            self.game_over()
    
    def flash_player(self):
        """Flash the player ship to indicate it was hit."""
        self.is_flashing = True
        flash_start_time = time.time()
        flash_duration = 1.5  # seconds
        flash_count = 6
        
        def do_flash():
            # Calculate how far we are into the flash sequence
            elapsed = time.time() - flash_start_time
            if elapsed >= flash_duration:
                # End of flash sequence - restore normal color
                self.canvas.itemconfig(self.player_ship, fill="#00FF00")
                self.is_flashing = False
                return
                
            # Flash between normal and blue
            flash_interval = flash_duration / flash_count
            flash_phase = int(elapsed / flash_interval) % 2
            
            if flash_phase == 0:
                self.canvas.itemconfig(self.player_ship, fill="#00FF00")  # Normal green
            else:
                self.canvas.itemconfig(self.player_ship, fill="#6666FF")  # Blue instead of red
                
            # Schedule next flash
            self.master.after(50, do_flash)
            
        # Start the flash sequence
        do_flash()
    
    def update_hud(self):
        """Update the HUD with current game values."""
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
        self.canvas.itemconfig(self.level_text, text=f"Level: {self.level}")
        self.canvas.itemconfig(self.shields_text, text=f"Shields: {self.shields}")
    
    def level_up(self):
        """Increase the game level and difficulty."""
        self.level += 1
        self.update_hud()
        
        # Increase enemy spawn rate and speed with level
        self.enemy_spawn_delay = max(500, 2000 - (self.level * 100))
        self.enemy_speed += 0.5
    
    def create_barriers(self):
        """Create Space Invaders style protective barriers."""
        # Barrier properties
        self.barriers = []
        self.barrier_blocks = []
        num_barriers = 4
        barrier_width = 70
        barrier_height = 50
        barrier_y = self.player_y - 80  # Position above player
        
        # Calculate spacing
        total_width = num_barriers * barrier_width
        spacing = (800 - total_width) / (num_barriers + 1)
        
        # Block size
        block_size = 8
        
        # Create each barrier
        for i in range(num_barriers):
            # Calculate barrier position
            barrier_x = spacing + (i * (barrier_width + spacing)) + barrier_width/2
            
            barrier_blocks = []
            
            # Define the shape of the barrier (fortress-like with a gap in the middle-top)
            # Each 1 in the pattern represents a block
            barrier_pattern = [
                [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
                [1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
                [1, 1, 1, 0, 0, 0, 0, 1, 1, 1]
            ]
            
            # Create blocks based on pattern
            for row_idx, row in enumerate(barrier_pattern):
                for col_idx, cell in enumerate(row):
                    if cell == 1:
                        # Calculate block position
                        block_x = barrier_x - barrier_width/2 + col_idx * block_size
                        block_y = barrier_y - barrier_height/2 + row_idx * block_size
                        
                        # Create block
                        block = self.canvas.create_rectangle(
                            block_x, block_y,
                            block_x + block_size, block_y + block_size,
                            fill="#44DD44",  # Green blocks
                            outline="#339933",
                            tags="barrier"
                        )
                        
                        # Store block with position data
                        barrier_blocks.append({
                            "id": block,
                            "x": block_x + block_size/2,
                            "y": block_y + block_size/2,
                            "health": 3  # Each block can take 3 hits
                        })
            
            # Add barrier to list
            self.barriers.append({
                "x": barrier_x,
                "y": barrier_y,
                "blocks": barrier_blocks
            })
            
            # Add all blocks to the list
            self.barrier_blocks.extend(barrier_blocks) 
    
    def check_bullet_hit_barrier(self, bullet_coords):
        """Check if a bullet hits a barrier and damage the barrier if hit."""
        if not bullet_coords or len(bullet_coords) < 4:
            return False
            
        # Calculate bullet center
        bullet_x = (bullet_coords[0] + bullet_coords[2]) / 2
        bullet_y = (bullet_coords[1] + bullet_coords[3]) / 2
        
        # Check each barrier block
        blocks_to_check = list(self.barrier_blocks)  # Use a copy of the list
        for block in blocks_to_check:
            try:
                # Skip destroyed blocks
                if block.get("health", 0) <= 0:
                    continue
                    
                # Get block position
                if "id" not in block:
                    continue
                    
                block_coords = self.canvas.coords(block["id"])
                if not block_coords:
                    continue  # Skip if block no longer exists
                    
                # Check if bullet is inside block
                if (bullet_x >= block_coords[0] and bullet_x <= block_coords[2] and
                    bullet_y >= block_coords[1] and bullet_y <= block_coords[3]):
                    # Hit! Reduce block health
                    block["health"] -= 1
                    
                    # Update block appearance based on health
                    if block["health"] <= 0:
                        # Destroy block
                        self.canvas.delete(block["id"])
                        if block in self.barrier_blocks:
                            self.barrier_blocks.remove(block)
                    elif block["health"] == 2:
                        # Slightly damaged
                        self.canvas.itemconfig(block["id"], fill="#339933", outline="#228822")
                    elif block["health"] == 1:
                        # Heavily damaged
                        self.canvas.itemconfig(block["id"], fill="#228822", outline="#117711")
                    
                    return True  # Collision detected
            except Exception as e:
                # Skip problematic blocks
                continue
                
        return False  # No collision

    def flash_screen(self, color="#6666FF"):
        """Flash the screen a specific color."""
        # Create a semi-transparent overlay
        overlay = self.canvas.create_rectangle(
            0, 0, 800, 600,  # Fixed hard-coded dimensions instead of self.width/height
            fill=color,
            stipple="gray50",  # Makes it semi-transparent
            tags=["overlay"]
        )
        
        # Schedule removal after a short delay
        self.master.after(100, lambda: self.canvas.delete(overlay))
        
    def get_enemy_types(self):
        """Return different enemy types."""
        # Define different enemy types with more vibrant colors, no red or yellow dots
        return [
            {"fill": "#00FFFF", "outline": "#00FFFF", "size": 24, "shape": "alien1", "points": 10},  # Cyan enemy (top row)
            {"fill": "#00FF88", "outline": "#00FF88", "size": 22, "shape": "alien2", "points": 20},  # Green enemy (second row)
            {"fill": "#0088FF", "outline": "#0088FF", "size": 20, "shape": "alien3", "points": 30},  # Blue enemy (third row)
            {"fill": "#8800FF", "outline": "#8800FF", "size": 19, "shape": "alien4", "points": 40},  # Purple enemy (fourth row)
            {"fill": "#6666FF", "outline": "#6666FF", "size": 18, "shape": "alien5", "points": 50}   # Blue mothership (bottom row) - was red
        ]
        
    def create_enemy_bullet(self, x, y):
        """Create a bullet fired by an enemy."""
        try:
            # Create enemy bullet (blue instead of red)
            bullet = self.canvas.create_rectangle(
                x - 2, y, x + 2, y + 10,
                fill="#6666FF",  # Blue color (was red)
                outline="#99AAFF",  # Lighter blue outline (was light red)
                tags=["enemy_bullet"]
            )
            
            # Add slight random angle to bullet trajectory
            angle = random.uniform(-0.2, 0.2)  # Small random angle
            speed = self.enemy_bullet_speed
            dx = math.sin(angle) * speed
            dy = math.cos(angle) * speed
            
            # Store bullet with its velocity components
            self.enemy_bullets.append({
                "id": bullet,
                "dx": dx,
                "dy": dy
            })
            
            # Play sound effect
            self.play_sound("enemy_shoot")
            return True
        except Exception as e:
            print(f"Error creating enemy bullet: {e}")
            return False

    def draw_danger_warning(self, enemy_x, enemy_y):
        """Draw a warning indicator when enemies get too close."""
        warning = self.canvas.create_text(
            enemy_x, self.height - 30,
            text="⚠ DANGER ⚠",
            font=("Arial", 14, "bold"),
            fill="#6666FF",  # Blue instead of red
            tags=["danger_warning"]
        )
        
        # Pulse the warning message
        self._pulse_warning(warning, 1)
        
    def create_special_particle(self, x, y, event_type):
        """Create special particle effects for game events."""
        # Different particle styles based on event type
        if event_type == "explosion":
            colors = ["#0066FF", "#6699FF", "#99CCFF", "#FFFFFF"]  # Blue explosion (was red)
            count = 15
            max_speed = 5
            size_range = (3, 8)
            life = 20
        elif event_type == "powerup":
            colors = ["#00FFFF", "#0088FF", "#0044FF", "#FFFFFF"]  # Cyan/blue powerup
            count = 10
            max_speed = 3
            size_range = (2, 5)
            life = 15
            
        # Create particles
        for _ in range(count):
            size = random.randint(*size_range)
            color = random.choice(colors)
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, max_speed)
            
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            
            particle = {
                'shape': self.canvas.create_oval(
                    x-size, y-size, x+size, y+size,
                    fill=color, outline=""
                ),
                'dx': dx,
                'dy': dy,
                'life': life,
                'max_life': life,
                'size': size
            }
            
            self.particles.append(particle)
            
    # Color constants for the rainbow effect
    def get_rainbow_colors(self):
        """Return a list of rainbow colors (omitting red and yellow)."""
        return [
            "#0088FF", "#00AAFF", "#00FFFF", 
            "#00FFAA", "#00FF00", "#0088AA",
            "#0066FF", "#6666FF", "#9966FF", "#CC66FF"
        ]
        
    def _update_special_effects(self):
        """Update all special effects in the game."""
        # Update rainbow effect for the title
        if hasattr(self, 'title_text') and self.title_text:
            # Use blue-based rainbow colors instead of full spectrum with red
            rainbow_colors = self.get_rainbow_colors()
            current_time = time.time()
            color_index = int((current_time * 5) % len(rainbow_colors))
            self.canvas.itemconfig(self.title_text, fill=rainbow_colors[color_index])
            
        # Implement other special effects as needed 

    def _check_condition_and_highlight(self, condition, widget_id):
        """Check a condition and highlight a widget if true."""
        if condition:
            # Highlight by flashing blue (was red)
            current_fill = self.canvas.itemcget(widget_id, "fill")
            self.canvas.itemconfig(widget_id, fill="#6666FF")
            self.master.after(300, lambda: self.canvas.itemconfig(widget_id, fill=current_fill))
            return True
        return False 

    def _filter_colors(self, item):
        """Filter out yellow and red colors from items."""
        try:
            fill = self.canvas.itemcget(item, "fill")
            if fill == 'yellow' or fill == 'red' or fill.startswith('#FF'):
                # It's a yellow or red item we want to filter out
                return True
            return False
        except:
            return False
            
    def play_sound(self, sound_type):
        """Play sound effects (stub method - would connect to actual sound system)."""
        # In a real implementation, this would play actual sounds
        print(f"Playing sound: {sound_type}")
        
    def _pulse_warning(self, warning_id, pulse_count):
        """Pulse a warning message."""
        if pulse_count > 6 or not self.game_running:
            self.canvas.delete(warning_id)
            return
            
        # Toggle visibility
        if pulse_count % 2 == 0:
            self.canvas.itemconfig(warning_id, state="normal")
        else:
            self.canvas.itemconfig(warning_id, state="hidden")
            
        # Schedule next pulse
        self.master.after(300, lambda: self._pulse_warning(warning_id, pulse_count + 1)) 