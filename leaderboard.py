#!/usr/bin/env python3
# Galactic Defenders - Leaderboard Module
# Handles leaderboard database and space facts

import sqlite3
import os
import random
from datetime import datetime

class LeaderboardManager:
    """Manages the leaderboard database and space facts for Galactic Defenders."""
    
    def __init__(self, db_path=None):
        """Initialize the leaderboard manager with a database path."""
        # Use default path if none provided
        if db_path is None:
            self.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gamedata.db")
        else:
            self.db_path = db_path
            
        # Initialize database
        self._init_database()
        
        # Load space facts
        self.space_facts = self._get_space_facts()
        
    def _init_database(self):
        """Initialize the SQLite database with the required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create leaderboard table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            score INTEGER NOT NULL,
            level INTEGER NOT NULL,
            date_time TEXT NOT NULL
        )
        ''')
        
        conn.commit()
        conn.close()
        
    def add_score(self, player_name, score, level):
        """Add a new score to the leaderboard."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get current date and time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Insert the new score
        cursor.execute(
            "INSERT INTO leaderboard (player_name, score, level, date_time) VALUES (?, ?, ?, ?)",
            (player_name, score, level, current_time)
        )
        
        conn.commit()
        conn.close()
        
    def get_top_scores(self, limit=10):
        """Get the top scores from the leaderboard."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get top scores ordered by score (highest first)
        cursor.execute(
            "SELECT player_name, score, level, date_time FROM leaderboard ORDER BY score DESC LIMIT ?",
            (limit,)
        )
        
        top_scores = cursor.fetchall()
        conn.close()
        
        return top_scores
        
    def get_player_rank(self, player_name, score):
        """Get the rank of a player based on their score."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Count how many scores are higher than this one
        cursor.execute(
            "SELECT COUNT(*) FROM leaderboard WHERE score > ?",
            (score,)
        )
        
        rank = cursor.fetchone()[0] + 1  # Add 1 because ranks start at 1
        conn.close()
        
        return rank
        
    def clear_leaderboard(self):
        """Clear all entries from the leaderboard."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM leaderboard")
        
        conn.commit()
        conn.close()
        
    def get_random_space_fact(self):
        """Return a random space fact."""
        return random.choice(self.space_facts)
        
    def _get_space_facts(self):
        """Return a list of interesting space facts."""
        return [
            "The Sun makes up 99.86% of the mass in our solar system.",
            "One million Earths could fit inside the Sun.",
            "The Sun's surface temperature is about 5,500°C (9,940°F).",
            "Light from the Sun takes about 8 minutes to reach Earth.",
            "The Milky Way galaxy is estimated to have 100-400 billion stars.",
            "The Milky Way is approximately 100,000 light-years across.",
            "There are more stars in the universe than grains of sand on Earth.",
            "A year on Mercury is just 88 Earth days.",
            "A day on Venus is longer than its year (243 Earth days vs 225).",
            "If you could drive to the Sun at 100 km/h, it would take 171 years.",
            "Jupiter has the shortest day of all the planets, rotating once every 9.8 hours.",
            "Jupiter's Great Red Spot is a storm that has lasted over 300 years.",
            "Saturn's rings are made mostly of ice particles, with some rocky debris.",
            "Neptune has the strongest winds in the solar system, reaching 2,100 km/h.",
            "There are more possible iterations in a game of chess than atoms in the universe.",
            "A black hole's gravitational pull is so strong that not even light can escape it.",
            "The universe is estimated to be around 13.8 billion years old.",
            "The observable universe is estimated to contain over 2 trillion galaxies.",
            "The coldest place in the universe is the Boomerang Nebula at -272°C (-458°F).",
            "About 1,000,000 Earth's could fit inside Jupiter.",
            "Mars' sunset appears blue due to how dust particles scatter light.",
            "One day on Saturn's moon Titan lasts about 16 Earth days.",
            "Pluto is smaller than the United States (width).",
            "The largest asteroid, Ceres, is also categorized as a dwarf planet.",
            "Space is completely silent as there is no air for sound waves to travel through.",
            "The footprints left by astronauts on the Moon will likely remain for at least 100 million years.",
            "The core of Jupiter is so pressurized that it's believed to contain a diamond the size of Earth.",
            "If a star passes too close to a black hole, it can be torn apart.",
            "The most massive star known is R136a1, with a mass about 315 times that of the Sun.",
            "In 3.75 billion years, the Milky Way and Andromeda galaxies will collide."
        ]
        
# For testing purposes
if __name__ == "__main__":
    # Test the leaderboard functionality
    lm = LeaderboardManager()
    print("Adding test scores...")
    lm.add_score("Test1", 500, 3)
    lm.add_score("Test2", 1000, 5)
    lm.add_score("Test3", 750, 4)
    
    print("Top scores:")
    for score in lm.get_top_scores():
        print(score)
        
    print("Random space fact:", lm.get_random_space_fact()) 