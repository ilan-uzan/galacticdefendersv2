#!/usr/bin/env python3
# Galactic Defenders - Space API Module
# Handles fetching space facts from public APIs

import requests
import random
import json

class SpaceAPI:
    def __init__(self):
        """Initialize the Space API client."""
        # Base URL for the Solar System OpenData API
        self.base_url = "https://api.le-systeme-solaire.net/rest/bodies"
        # Celestial bodies to choose from for random facts
        self.bodies = [
            "mercury", "venus", "earth", "mars", "jupiter", 
            "saturn", "uranus", "neptune", "pluto"
        ]
        
    def get_random_fact(self):
        """Get a random space fact from the API."""
        try:
            # Choose a random celestial body
            body = random.choice(self.bodies)
            response = requests.get(f"{self.base_url}/{body}")
            
            if response.status_code == 200:
                data = response.json()
                return self._format_fact(data)
            else:
                return self._get_fallback_fact()
        except Exception as e:
            print(f"Error fetching space fact: {e}")
            return self._get_fallback_fact()
    
    def get_fact(self, body="mars"):
        """Get a fact about a specific celestial body."""
        try:
            response = requests.get(f"{self.base_url}/{body}")
            
            if response.status_code == 200:
                data = response.json()
                return self._format_fact(data)
            else:
                return self._get_fallback_fact(body)
        except Exception as e:
            print(f"Error fetching space fact: {e}")
            return self._get_fallback_fact(body)
    
    def _format_fact(self, data):
        """Format the API response into a readable fact."""
        # Extract interesting data
        name = data.get("englishName", "Unknown")
        gravity = data.get("gravity", "Unknown")
        moons = data.get("moons", [])
        moon_count = len(moons) if moons else 0
        mass = data.get("mass", {}).get("massValue", "Unknown")
        mass_exp = data.get("mass", {}).get("massExponent", "")
        
        # Generate possible facts
        facts = []
        
        if name != "Unknown":
            if gravity != "Unknown":
                facts.append(f"{name} has a surface gravity of {gravity} m/s², compared to Earth's 9.8 m/s².")
            
            if moon_count > 0:
                if moon_count == 1:
                    moon_name = moons[0].get("moon", "a moon")
                    facts.append(f"{name} has one moon named {moon_name}.")
                else:
                    facts.append(f"{name} has {moon_count} moons orbiting it.")
            
            if mass != "Unknown":
                facts.append(f"The mass of {name} is {mass}×10^{mass_exp} kg.")
        
        # Return a random fact or a fallback
        if facts:
            return random.choice(facts)
        else:
            return self._get_fallback_fact(name)
    
    def _get_fallback_fact(self, body=None):
        """Return a fallback fact if the API request fails."""
        fallback_facts = [
            "Space is completely silent because there is no air to carry sound waves.",
            "A day on Venus is longer than a year on Venus.",
            "The Great Red Spot on Jupiter is a storm that has been raging for over 300 years.",
            "Saturn's rings are made mostly of ice and rock.",
            "A year on Mercury is just 88 Earth days.",
            "The Milky Way galaxy is on a collision course with the Andromeda galaxy.",
            "There are more stars in the universe than grains of sand on all the beaches on Earth."
        ]
        
        if body:
            body_facts = {
                "mercury": "Mercury is the smallest planet in our solar system.",
                "venus": "Venus is the hottest planet in our solar system.",
                "earth": "Earth is the only known planet with active plate tectonics.",
                "mars": "Mars has the largest dust storms in our solar system.",
                "jupiter": "Jupiter is the largest planet in our solar system.",
                "saturn": "Saturn has the most extensive ring system of any planet.",
                "uranus": "Uranus rotates on its side, unlike other planets.",
                "neptune": "Neptune has the strongest winds in our solar system.",
                "pluto": "Pluto is now classified as a dwarf planet."
            }
            
            return body_facts.get(body.lower(), random.choice(fallback_facts))
        else:
            return random.choice(fallback_facts) + "\n(Space Fact API unavailable. Try again!)" 