#!/usr/bin/env python3
# Galactic Defenders - Utilities Module
# Helper functions for collision detection, bullet cooldown, etc.

import math
import time

def check_collision(obj1, obj2):
    """
    Check if two objects (represented by their bounding boxes) are colliding.
    Each object should have x1, y1, x2, y2 attributes defining its bounding box.
    
    Args:
        obj1: First object with x1, y1, x2, y2 properties
        obj2: Second object with x1, y1, x2, y2 properties
        
    Returns:
        bool: True if colliding, False otherwise
    """
    # Check if obj1 is entirely to the left, right, above, or below obj2
    if (obj1["x2"] < obj2["x1"] or  # obj1 is left of obj2
        obj1["x1"] > obj2["x2"] or  # obj1 is right of obj2
        obj1["y2"] < obj2["y1"] or  # obj1 is above obj2
        obj1["y1"] > obj2["y2"]):   # obj1 is below obj2
        return False
    return True

class CooldownManager:
    """
    Manages cooldowns for game actions like shooting.
    
    Example usage:
        cooldown = CooldownManager()
        # In game loop:
        if cooldown.can_fire("player_shoot"):
            # Fire bullet
            cooldown.start_cooldown("player_shoot", 0.5)  # 500ms cooldown
    """
    def __init__(self):
        """Initialize the cooldown manager."""
        self.cooldowns = {}
    
    def start_cooldown(self, action_name, cooldown_time):
        """
        Start a cooldown for the given action.
        
        Args:
            action_name (str): Identifier for the action
            cooldown_time (float): Cooldown time in seconds
        """
        self.cooldowns[action_name] = time.time() + cooldown_time
    
    def can_fire(self, action_name):
        """
        Check if an action is ready to be performed (cooldown expired).
        
        Args:
            action_name (str): Identifier for the action
            
        Returns:
            bool: True if action is ready (no cooldown), False otherwise
        """
        if action_name not in self.cooldowns:
            return True
        
        current_time = time.time()
        return current_time >= self.cooldowns[action_name]
    
    def get_remaining_time(self, action_name):
        """
        Get the remaining cooldown time for an action.
        
        Args:
            action_name (str): Identifier for the action
            
        Returns:
            float: Remaining time in seconds, or 0 if ready
        """
        if action_name not in self.cooldowns:
            return 0
        
        current_time = time.time()
        remaining = self.cooldowns[action_name] - current_time
        
        return max(0, remaining)

def calculate_distance(x1, y1, x2, y2):
    """
    Calculate the Euclidean distance between two points.
    
    Args:
        x1, y1: Coordinates of the first point
        x2, y2: Coordinates of the second point
        
    Returns:
        float: Distance between the points
    """
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def calculate_angle(x1, y1, x2, y2):
    """
    Calculate the angle between two points (in radians).
    
    Args:
        x1, y1: Coordinates of the first point
        x2, y2: Coordinates of the second point
        
    Returns:
        float: Angle in radians
    """
    return math.atan2(y2 - y1, x2 - x1)

def clamp(value, min_value, max_value):
    """
    Clamp a value between min and max bounds.
    
    Args:
        value: The value to clamp
        min_value: Minimum allowed value
        max_value: Maximum allowed value
        
    Returns:
        The clamped value
    """
    return max(min_value, min(value, max_value))

def get_elapsed_time_formatted(start_time):
    """
    Format elapsed time since start_time in MM:SS format.
    
    Args:
        start_time: Starting time (from time.time())
        
    Returns:
        str: Formatted time string "MM:SS"
    """
    elapsed = time.time() - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    return f"{minutes:02d}:{seconds:02d}" 