import pygame
from game.enemy import Enemy
from game.ranged_enemy import RangedEnemy
from random import randint, uniform
from game.settings import Settings, GameSettings
from game.enemy_stats import EnemyStats
from game.enemy_type import EnemyType, BasicEnemy, FastEnemy, TankEnemy, RangedEnemy as RangedEnemyType, BossEnemy
from tests.test_config import test_config
from testing import log
import math

class WaveManager:
    def __init__(self, settings: Settings, particle_group, tower_x: float, tower_y: float, tower_range: int, enemy_projectiles: pygame.sprite.Group):
        self.settings = settings
        self.particle_group = particle_group
        self.tower_x = tower_x
        self.tower_y = tower_y
        self.tower_range = tower_range
        self.enemy_projectiles = enemy_projectiles
        self.screen_width = settings.get_window_width()
        self.screen_height = settings.get_window_height()
        
        # Apply test config for initial wave
        if test_config.enabled and test_config.initial_wave:
            self.wave_number = test_config.initial_wave
            self.round_number = test_config.initial_round if test_config.initial_round else 0
        else:
            self.wave_number = 1
            self.round_number = 0
        
        # Apply test config for enemies per round
        if test_config.enabled and test_config.enemies_per_round is not None:
            self.enemies_per_round = test_config.enemies_per_round
        else:
            self.enemies_per_round = 5
        
        self.round_timer = 0
        
        # Apply test config for round delay
        if test_config.enabled and test_config.round_delay is not None:
            self.round_delay = test_config.round_delay
        else:
            self.round_delay = 2000  # 2 seconds between rounds
        
        self.skip = False
        self.enemy_stats = EnemyStats()
        
        # Update enemy stats to match initial wave
        if self.wave_number > 1:
            self.enemy_stats.update_attack(self.wave_number)
            self.enemy_stats.update_health(self.wave_number)
        
        self.boss_spawned = False

    def update(self):
        # Apply test config game speed multiplier
        time_delta = 16  # Base time for 60 FPS
        if test_config.enabled and test_config.game_speed_multiplier:
            time_delta = int(time_delta * test_config.game_speed_multiplier)
        
        self.round_timer += time_delta
        if self.round_timer >= self.round_delay:
            self.round_timer = 0
            self.round_number += 1
            if self.round_number > 10:
                # Start new wave
                self.round_number = 1
                self.wave_number += 1

                # Will have logic for wave skipping here, for now just spawn next wave immediately
                self.enemy_stats.update_attack(self.wave_number)
                self.enemy_stats.update_health(self.wave_number)
                self.boss_spawned = False

            return self.spawn_round()
        return pygame.sprite.Group()

    def spawn_round(self):
        enemies = pygame.sprite.Group()
        for _ in range(self.enemies_per_round):
            # Spawn at 100m radius from tower, random angle
            spawn_radius_pixels = GameSettings.enemy_spawn_radius * GameSettings.pixels_per_meter
            angle = uniform(0, 2 * math.pi)
            
            # Calculate spawn position
            x = self.tower_x + spawn_radius_pixels * math.cos(angle)
            y = self.tower_y + spawn_radius_pixels * math.sin(angle)
            
            # Clamp to screen edges if off-screen
            x = max(0, min(x, self.screen_width))
            y = max(0, min(y, self.screen_height))
            
            enemy = self.pick_enemy(x, y)
            log("WAVE", f"SPAWNING: {enemy}")
            enemies.add(enemy)
            log("WAVE", f"WAVEMANAGER RETURNING: {enemies}")
        return enemies
    
    def pick_enemy(self, x, y):
        # Check if test config forces a specific enemy type
        if test_config.enabled and test_config.force_enemy_type:
            enemy_type = test_config.force_enemy_type
            log("WAVE", f"Test mode: forcing enemy type {enemy_type}")
        else:
            # Normal random enemy selection
            pick = randint(1, 100)
            boss_round = randint(1, 10)

            if self.wave_number % 10 == 0:
                if (boss_round == self.round_number and not self.boss_spawned) or \
                (self.round_number == 10 and not self.boss_spawned):
                    self.boss_spawned = True
                    log("WAVE", f"SPAWNING BOSS ENEMY!")
                    return Enemy(x, y, self.tower_x, self.tower_y,
                                    self.wave_number, BossEnemy(),
                                    self.enemy_stats, self.particle_group)

            cumulative = 0
            enemy_type = ""
            for etype, chance in self.chances(self.wave_number).items():
                cumulative += chance
                if pick <= cumulative:
                    log("WAVE", f"Picked enemy type: {etype} (roll: {pick} <= {cumulative})")
                    enemy_type = etype
                    break

        enemy_classes = {
            "basic": BasicEnemy,
            "fast": FastEnemy,
            "tank": TankEnemy,
            "ranged": RangedEnemyType
        }

        # Instantiate ranged enemy with special class, others use base Enemy
        if enemy_type == "ranged":
            return RangedEnemy(
                x, y,
                self.tower_x, self.tower_y,
                self.wave_number,
                enemy_classes[enemy_type](),
                self.enemy_stats,
                self.particle_group,
                self.tower_range,
                self.enemy_projectiles
            )
        else:
            return Enemy(
                x, y,
                self.tower_x, self.tower_y,
                self.wave_number,
                enemy_classes[enemy_type](),
                self.enemy_stats,
                self.particle_group
            )


    def chances(self, wave):
        # Example: Return a dictionary of enemy types and their spawn chances based on the wave number
        chances = {
            "basic": 95,
            "fast": 5,
            "tank": 0,
            "ranged": 0}
        
        if wave >= 3:
            chances["basic"] -= 2
            chances["tank"] += 2

        if wave >= 6:
            chances["basic"] -= 4
            chances["fast"] += 1
            chances["tank"] += 2
            chances["ranged"] += 1
        
        if wave >= 20:
            twenties = wave // 20
            chances["basic"] = min(25, chances["basic"] - 4 * twenties)
            chances["fast"] = max(25, chances["fast"] + 1 * twenties)
            chances["tank"] = max(25, chances["tank"] + 2 * twenties)
            chances["ranged"] = max(25, chances["ranged"] + 1 * twenties)

        return chances