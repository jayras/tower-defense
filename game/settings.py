import json
from pathlib import Path
from random import random

# Game Settings
class GameSettings:
    window_width = 1280
    window_height = 720
    fullscreen = False
    debug = True
    splash_damage_percent = 0.5
    game_speed = 1.0
    game_speed_step = 0.5
    game_speed_max = 5.0
    pixels_per_meter = 5
    
    # Tower range upgrade constants
    tower_range_per_level = 0.5  # meters per upgrade level
    tower_range_max_level = 79  # max upgrade levels
    
    # Enemy spawn constants
    enemy_spawn_radius = 100  # meters from tower center

# -----------------------------
#  Core Layer (Hardcoded Defaults)
# -----------------------------
class CoreSettings:
    multishot_chance = 0.0
    multishot_targets = 1
    crit_chance = 0.0
    splash_radius = 0.0
    pierce = 0
    projectile_speed = 8.0
    crit_multiplier = 1.5
    projectile_damage = 10.0
    tower_max_health = 100
    tower_range = 30  # meters


# -----------------------------
#  In-Run Layer (Temporary)
# -----------------------------
class InGameSettings:
    def __init__(self):
        self.multishot_chance = 0.0
        self.multishot_targets = 0
        self.crit_chance = 0.0
        self.splash_radius = 0.0
        self.pierce = 0
        self.projectile_speed = 0.0
        self.crit_multiplier = 0.0
        self.projectile_damage = 0.0
        self.tower_max_health = 0
        self.tower_range = 0

# -----------------------------
#  Workshop Layer (Permanent Player Upgrades)
# -----------------------------
class WorkshopSettings:
    def __init__(self, data):
        self.multishot_chance = data.get("multishot_chance", 0.0)
        self.multishot_targets = data.get("multishot_targets", 0)
        self.crit_chance = data.get("crit_chance", 0.0)
        self.splash_radius = data.get("splash_radius", 0.0)
        self.pierce = data.get("pierce", 0)
        self.projectile_speed = data.get("projectile_speed", 0.0)
        self.crit_multiplier = data.get("crit_multiplier", 0.0)
        self.projectile_damage = data.get("projectile_damage", 0.0)
        self.tower_max_health = data.get("tower_max_health", 0)
        self.tower_range = data.get("tower_range", 0)

    def to_dict(self):
        return {
            "multishot_chance": self.multishot_chance,
            "multishot_targets": self.multishot_targets,
            "crit_chance": self.crit_chance,
            "splash_radius": self.splash_radius,
            "pierce": self.pierce,
            "projectile_speed": self.projectile_speed,
            "crit_multiplier": self.crit_multiplier,
            "projectile_damage": self.projectile_damage,
            "tower_max_health": self.tower_max_health,
            "tower_range": self.tower_range,
        }


# -----------------------------
#  Lab Layer (Permanent Meta-Rates)
# -----------------------------
class LabSettings:
    def __init__(self, data):
        self.multishot_rate = data.get("multishot_rate", 1.0)
        self.multishot_targets_rate = data.get("multishot_targets_rate", 1.0)
        self.crit_rate = data.get("crit_rate", 1.0)
        self.splash_rate = data.get("splash_rate", 1.0)
        self.pierce_rate = data.get("pierce_rate", 1.0)
        self.projectile_speed_rate = data.get("projectile_speed_rate", 1.0)
        self.crit_multiplier_rate = data.get("crit_multiplier_rate", 1.0)
        self.projectile_damage_rate = data.get("projectile_damage_rate", 1.0)
        self.tower_max_health_rate = data.get("tower_max_health_rate", 1.0)
        self.tower_range_rate = data.get("tower_range_rate", 1.0)

    def to_dict(self):
        return {
            "multishot_rate": self.multishot_rate,
            "multishot_targets_rate": self.multishot_targets_rate,
            "crit_rate": self.crit_rate,
            "splash_rate": self.splash_rate,
            "pierce_rate": self.pierce_rate,
            "projectile_speed_rate": self.projectile_speed_rate,
            "crit_multiplier_rate": self.crit_multiplier_rate,
            "projectile_damage_rate": self.projectile_damage_rate,
            "tower_max_health_rate": self.tower_max_health_rate,
            "tower_range_rate": self.tower_range_rate,
        }


# -----------------------------
#  Settings Wrapper (Final Computed Stats)
# -----------------------------
class Settings:
    def __init__(self, config_path="settings.json"):
        self.config_path = Path(config_path)

        # Load config file (or create defaults)
        config_data = self._load_config()

        self.core = CoreSettings()
        self.ingame = InGameSettings()
        self.workshop = WorkshopSettings(config_data.get("workshop", {}))
        self.lab = LabSettings(config_data.get("lab", {}))

    # -------------------------
    #  Computed Stat Getters
    # -------------------------
    def get_multishot_triggered(self) -> bool:
        """Determine if multishot triggers this frame."""
        base = self.core.multishot_chance
        run = self.ingame.multishot_chance
        perm = self.workshop.multishot_chance
        rate = self.lab.multishot_rate
        chance = ((perm + run) * rate) + base
        return random() < chance

    def get_crit_chance(self):
        base = self.core.crit_chance
        run = self.ingame.crit_chance
        perm = self.workshop.crit_chance
        rate = self.lab.crit_rate
        return ((perm + run) * rate) + base

    def get_splash_radius(self):
        base = self.core.splash_radius
        run = self.ingame.splash_radius
        perm = self.workshop.splash_radius
        rate = self.lab.splash_rate
        return ((perm + run) * rate) + base

    def get_projectile_speed(self):
        base = self.core.projectile_speed
        run = self.ingame.projectile_speed
        perm = self.workshop.projectile_speed
        rate = self.lab.projectile_speed_rate
        return ((perm + run) * rate) + base
    
    def get_crit_multiplier(self):
        base = self.core.crit_multiplier
        run = self.ingame.crit_multiplier
        perm = self.workshop.crit_multiplier
        rate = self.lab.crit_multiplier_rate
        return ((perm + run) * rate) + base
    
    def get_projectile_damage(self):
        base = self.core.projectile_damage
        run = self.ingame.projectile_damage
        perm = self.workshop.projectile_damage
        rate = self.lab.projectile_damage_rate
        damage = ((perm + run) * rate) + base

        # Crit calculation
        if self.get_crit_chance() > 0 and random() < self.get_crit_chance():
            damage *= self.get_crit_multiplier()
        return damage


    def get_splash_damage(self):
        # Splash damage is a static percentage of the projectile damage.
        pct = GameSettings.splash_damage_percent
        return self.get_projectile_damage() * pct

    def get_pierce(self):
        base = self.core.pierce
        run = self.ingame.pierce
        perm = self.workshop.pierce
        rate = self.lab.pierce_rate
        return int(((perm + run) * rate) + base)

    def get_multishot_targets(self):
        base = self.core.multishot_targets
        run = self.ingame.multishot_targets
        perm = self.workshop.multishot_targets
        rate = self.lab.multishot_targets_rate
        return int(((perm + run) * rate) + base)

    def get_tower_max_health(self):
        base = self.core.tower_max_health
        run = self.ingame.tower_max_health
        perm = self.workshop.tower_max_health
        rate = self.lab.tower_max_health_rate
        return int(((perm + run) * rate) + base)

    def get_tower_range(self):
        base = self.core.tower_range
        run = self.ingame.tower_range
        perm = self.workshop.tower_range
        rate = self.lab.tower_range_rate
        meters = int(((perm + run) * rate) + base)
        return meters * GameSettings.pixels_per_meter

    def get_window_width(self):
        return GameSettings.window_width
    
    def get_window_height(self):
        return GameSettings.window_height

    # -------------------------
    #  Config Load/Save
    # -------------------------
    def _load_config(self):
        if not self.config_path.exists():
            return {"workshop": {}, "lab": {}}

        with open(self.config_path, "r") as f:
            return json.load(f)

    def save(self):
        data = {
            "workshop": self.workshop.to_dict(),
            "lab": self.lab.to_dict(),
        }
        with open(self.config_path, "w") as f:
            json.dump(data, f, indent=4)
