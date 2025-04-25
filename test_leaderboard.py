#!/usr/bin/env python3
# Test script for leaderboard and space facts

import tkinter as tk
import os
from leaderboard import LeaderboardManager

def test_leaderboard():
    """Test basic leaderboard functionality."""
    print("Testing leaderboard functionality...")
    
    # Create a test database file
    test_db = "test_leaderboard.db"
    
    # Remove test database if it exists
    if os.path.exists(test_db):
        os.remove(test_db)
    
    # Create a leaderboard manager with the test database
    lm = LeaderboardManager(test_db)
    
    # Add some test scores
    test_data = [
        ("Player1", 1000, 5),
        ("Player2", 1500, 7),
        ("Player3", 500, 3),
        ("Player4", 2000, 10),
        ("Player5", 750, 4)
    ]
    
    for name, score, level in test_data:
        lm.add_score(name, score, level)
        print(f"Added score: {name}, {score}, {level}")
    
    # Get top scores
    top_scores = lm.get_top_scores()
    print("\nTop scores:")
    for i, (name, score, level, date) in enumerate(top_scores):
        print(f"{i+1}. {name}: {score} pts (Level {level}) - {date}")
    
    # Get player ranks
    print("\nPlayer ranks:")
    for name, score, level in test_data:
        rank = lm.get_player_rank(name, score)
        print(f"{name} (Score: {score}) - Rank: #{rank}")
    
    # Test space facts
    print("\nTesting space facts...")
    for _ in range(3):
        fact = lm.get_random_space_fact()
        print(f"Random fact: {fact}")
    
    # Clean up test database
    if os.path.exists(test_db):
        os.remove(test_db)
        print("\nTest database removed.")
    
    print("Leaderboard tests completed.")

def test_game_over_ui():
    """Test the game over UI with leaderboard integration."""
    print("Testing game over UI...")
    
    # Create a sample Tkinter window
    root = tk.Tk()
    root.title("Game Over UI Test")
    root.geometry("800x600")
    
    canvas = tk.Canvas(root, width=800, height=600, bg="black")
    canvas.pack(fill="both", expand=True)
    
    # Create a leaderboard manager
    lm = LeaderboardManager()
    
    # Add some test scores
    lm.add_score("Player1", 1000, 5)
    lm.add_score("Player2", 1500, 7)
    lm.add_score("Player3", 500, 3)
    lm.add_score("TestPlayer", 2000, 10)
    lm.add_score("Player5", 750, 4)
    
    # Get top scores and other data
    top_scores = lm.get_top_scores(5)
    player_rank = lm.get_player_rank("TestPlayer", 2000)
    space_fact = lm.get_random_space_fact()
    
    # Show game over message
    canvas.create_text(
        400, 150,
        text="GAME OVER",
        fill="#6666FF",
        font=("Courier", 36, "bold")
    )
    
    # Show player score
    canvas.create_text(
        400, 200,
        text=f"Final Score: 2000",
        fill="#FFFFFF",
        font=("Courier", 24)
    )
    
    # Show player rank
    canvas.create_text(
        400, 230,
        text=f"Rank: #{player_rank}",
        fill="#00FFAA",
        font=("Courier", 18)
    )
    
    # Show space fact header
    canvas.create_text(
        400, 270,
        text="SPACE FACT:",
        fill="#00FFFF",
        font=("Courier", 14, "bold")
    )
    
    # Show space fact
    fact_text = canvas.create_text(
        400, 295,
        text=space_fact,
        fill="#CCCCFF",
        font=("Courier", 12),
        width=600,
        justify=tk.CENTER
    )
    
    # Draw a separator line
    canvas.create_line(200, 320, 600, 320, fill="#444444", width=2)
    
    # Leaderboard title
    canvas.create_text(
        400, 340,
        text="TOP SCORES",
        fill="#00FF88",
        font=("Courier", 16, "bold")
    )
    
    # Display leaderboard entries
    y_pos = 370
    for i, (name, score, level, date) in enumerate(top_scores):
        # Highlight the current player's score
        is_player = name == "TestPlayer" and score == 2000
        color = "#FFFF00" if is_player else "#FFFFFF"
        
        # Format the leaderboard entry
        entry_text = f"{i+1}. {name}: {score} pts (Level {level})"
        
        canvas.create_text(
            400, y_pos,
            text=entry_text,
            fill=color,
            font=("Courier", 14)
        )
        y_pos += 25
    
    # Play again prompt
    canvas.create_text(
        400, 550,
        text="Press SPACE to play again",
        fill="#00FF00",
        font=("Courier", 16)
    )
    
    # Add a key binding to exit the test
    root.bind("<Escape>", lambda e: root.destroy())
    
    # Add a label with instructions for the test
    canvas.create_text(
        400, 580,
        text="Press ESC to exit test",
        fill="#888888",
        font=("Courier", 10)
    )
    
    print("Game over UI displayed. Close the window to continue.")
    root.mainloop()
    print("Game over UI test completed.")

if __name__ == "__main__":
    print("Leaderboard and Space Facts Test Suite")
    print("="*40)
    
    # Run the tests
    test_leaderboard()
    print("\n" + "="*40 + "\n")
    test_game_over_ui()
    
    print("\nAll tests completed.") 