import json
from pathlib import Path

# Game Settings
class GameSettings:
    window_width = 1280
    window_height = 720
    fullscreen = False


# -----------------------------
#  Core Layer (Hardcoded Defaults)
# -----------------------------
class CoreSettings:
    multishot_chance = 0.0
    crit_chance = 0.0
    splash_radius = 0.0


# -----------------------------
#  In-Run Layer (Temporary)
# -----------------------------
class InGameSettings:
    def __init__(self):
        self.multishot_chance = 0.0
        self.crit_chance = 0.0
        self.splash_radius = 0.0


# -----------------------------
#  Workshop Layer (Permanent Player Upgrades)
# -----------------------------
class WorkshopSettings:
    def __init__(self, data):
        self.multishot_chance = data.get("multishot_chance", 0.0)
        self.crit_chance = data.get("crit_chance", 0.0)
        self.splash_radius = data.get("splash_radius", 0.0)

    def to_dict(self):
        return {
            "multishot_chance": self.multishot_chance,
            "crit_chance": self.crit_chance,
            "splash_radius": self.splash_radius,
        }


# -----------------------------
#  Lab Layer (Permanent Meta-Rates)
# -----------------------------
class LabSettings:
    def __init__(self, data):
        self.multishot_rate = data.get("multishot_rate", 1.0)
        self.crit_rate = data.get("crit_rate", 1.0)
        self.splash_rate = data.get("splash_rate", 1.0)

    def to_dict(self):
        return {
            "multishot_rate": self.multishot_rate,
            "crit_rate": self.crit_rate,
            "splash_rate": self.splash_rate,
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
    def get_multishot_chance(self):
        base = self.core.multishot_chance
        run = self.ingame.multishot_chance
        perm = self.workshop.multishot_chance
        rate = self.lab.multishot_rate
        return (base + perm + run) * rate

    def get_crit_chance(self):
        base = self.core.crit_chance
        run = self.ingame.crit_chance
        perm = self.workshop.crit_chance
        rate = self.lab.crit_rate
        return (base + perm + run) * rate

    def get_splash_radius(self):
        base = self.core.splash_radius
        run = self.ingame.splash_radius
        perm = self.workshop.splash_radius
        rate = self.lab.splash_rate
        return (base + perm + run) * rate

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
