"""
Test configuration and scenarios for debugging and automated testing.
Allows launching the game in specific states without menu interaction.
"""

class TestConfig:
    """Configuration for test mode."""
    
    def __init__(self):
        # Test mode settings
        self.enabled = False
        self.auto_start = False  # Skip menu and start game immediately
        
        # Initial game state
        self.initial_wave = 1
        self.initial_round = 0
        self.tower_health = None  # None = use default from settings
        
        # Enemy spawning
        self.force_enemy_type = None  # None or "basic", "fast", "tank", "ranged", "boss"
        self.enemies_per_round = None  # None = use default
        
        # Time controls
        self.game_speed_multiplier = 1.0  # Speed up game time
        self.round_delay = None  # Override round delay in ms (None = use default)
        
        # Debug features
        self.invincible_tower = False  # Tower takes no damage
        self.one_hit_kill = False  # All enemies die in one hit
        self.infinite_range = False  # Tower has infinite range
        self.show_debug_info = False  # Show extra debug overlay
        
        # Auto-actions
        self.auto_upgrade = None  # Automatically apply upgrades (dict of stat: value)
    
    def apply_scenario(self, scenario_name: str):
        """Apply a predefined test scenario."""
        scenarios = {
            "quick_start": {
                "auto_start": True,
                "game_speed_multiplier": 2.0,
                "round_delay": 500,
            },
            "wave_10": {
                "auto_start": True,
                "initial_wave": 10,
                "show_debug_info": True,
            },
            "ranged_test": {
                "auto_start": True,
                "initial_wave": 6,
                "force_enemy_type": "ranged",
                "enemies_per_round": 3,
                "round_delay": 1000,
            },
            "tank_test": {
                "auto_start": True,
                "force_enemy_type": "tank",
                "enemies_per_round": 2,
                "round_delay": 2000,
            },
            "boss_test": {
                "auto_start": True,
                "initial_wave": 10,
                "force_enemy_type": "boss",
                "enemies_per_round": 1,
                "round_delay": 5000,
            },
            "invincible": {
                "auto_start": True,
                "invincible_tower": True,
                "show_debug_info": True,
            },
            "god_mode": {
                "auto_start": True,
                "invincible_tower": True,
                "one_hit_kill": True,
                "infinite_range": True,
                "show_debug_info": True,
            },
            "fast_debug": {
                "auto_start": True,
                "game_speed_multiplier": 5.0,
                "round_delay": 200,
                "show_debug_info": True,
            },
        }
        
        if scenario_name in scenarios:
            self.enabled = True
            config = scenarios[scenario_name]
            for key, value in config.items():
                setattr(self, key, value)
            return True
        return False
    
    def list_scenarios(self):
        """Return list of available scenario names."""
        return [
            "quick_start - Fast game with 2x speed",
            "wave_10 - Start at wave 10",
            "ranged_test - Test ranged enemies",
            "tank_test - Test tank enemies",
            "boss_test - Test boss enemy",
            "invincible - Tower cannot die",
            "god_mode - Invincible tower + one-hit kills + infinite range",
            "fast_debug - 5x speed for rapid testing",
        ]


# Global test config instance
test_config = TestConfig()
