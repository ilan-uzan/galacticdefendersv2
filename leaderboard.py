#!/usr/bin/env python3
# Galactic Defenders - Leaderboard Module
# Handles SQLite leaderboard and score tracking

import sqlite3
import json
import os
from datetime import datetime

class Leaderboard:
    def __init__(self, db_path="leaderboard.db", json_path="leaderboard.json"):
        """Initialize the leaderboard with SQLite database."""
        self.db_path = db_path
        self.json_path = json_path
        self.initialize_db()
        
    def initialize_db(self):
        """Create the SQLite database if it doesn't exist."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create leaderboard table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS leaderboard (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    timestamp TEXT NOT NULL
                )
            ''')
            
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            # Fall back to JSON if SQLite fails
            self.use_json_fallback()
            
    def add_score(self, name, score):
        """Add a new score to the leaderboard."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO leaderboard (name, score, timestamp) VALUES (?, ?, ?)",
                (name, score, timestamp)
            )
            
            conn.commit()
            conn.close()
            
            # Also update JSON backup
            self.backup_to_json()
            
            return True
        except sqlite3.Error as e:
            print(f"Error adding score to SQLite: {e}")
            return self.add_score_to_json(name, score, timestamp)
    
    def get_top_scores(self, limit=5):
        """Get the top N scores from the leaderboard."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT name, score, timestamp FROM leaderboard ORDER BY score DESC LIMIT ?",
                (limit,)
            )
            
            scores = cursor.fetchall()
            conn.close()
            
            return scores
        except sqlite3.Error as e:
            print(f"Error retrieving scores from SQLite: {e}")
            return self.get_top_scores_from_json(limit)
    
    def backup_to_json(self):
        """Create a JSON backup of the leaderboard."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT name, score, timestamp FROM leaderboard")
            scores = cursor.fetchall()
            
            leaderboard_data = {
                "scores": [
                    {"name": name, "score": score, "timestamp": timestamp}
                    for name, score, timestamp in scores
                ]
            }
            
            with open(self.json_path, 'w') as f:
                json.dump(leaderboard_data, f, indent=2)
                
            conn.close()
        except Exception as e:
            print(f"Error backing up to JSON: {e}")
    
    def use_json_fallback(self):
        """Check if JSON backup exists and initialize if needed."""
        if not os.path.exists(self.json_path):
            # Create a new empty JSON file
            with open(self.json_path, 'w') as f:
                json.dump({"scores": []}, f, indent=2)
    
    def add_score_to_json(self, name, score, timestamp):
        """Add a score to the JSON backup file."""
        try:
            if os.path.exists(self.json_path):
                with open(self.json_path, 'r') as f:
                    leaderboard_data = json.load(f)
            else:
                leaderboard_data = {"scores": []}
            
            leaderboard_data["scores"].append({
                "name": name,
                "score": score,
                "timestamp": timestamp
            })
            
            with open(self.json_path, 'w') as f:
                json.dump(leaderboard_data, f, indent=2)
                
            return True
        except Exception as e:
            print(f"Error adding score to JSON: {e}")
            return False
    
    def get_top_scores_from_json(self, limit=5):
        """Get top scores from the JSON backup."""
        try:
            if not os.path.exists(self.json_path):
                return []
                
            with open(self.json_path, 'r') as f:
                leaderboard_data = json.load(f)
            
            # Sort scores and get top N
            sorted_scores = sorted(
                leaderboard_data["scores"], 
                key=lambda x: x["score"], 
                reverse=True
            )
            
            top_scores = sorted_scores[:limit]
            
            # Convert to same format as SQLite response
            return [
                (entry["name"], entry["score"], entry["timestamp"])
                for entry in top_scores
            ]
        except Exception as e:
            print(f"Error reading JSON leaderboard: {e}")
            return [] 