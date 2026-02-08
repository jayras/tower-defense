import pygame
from game.enemy import Enemy
from random import randint, uniform
from game.settings import Settings, GameSettings
from testing import log
import math

class WaveManager:
    def __init__(self, settings: Settings, particle_group, tower_x: float, tower_y: float):
        self.settings = settings
        self.particle_group = particle_group
        self.tower_x = tower_x
        self.tower_y = tower_y
        self.screen_width = settings.get_window_width()
        self.screen_height = settings.get_window_height()
        self.wave_number = 0
        self.round_number = 0
        self.enemies_per_round = 5
        self.round_timer = 0
        self.round_delay = 2000  # 2 seconds between rounds

    def update(self):
        self.round_timer += 16  # Approximate for 60 FPS
        if self.round_timer >= self.round_delay:
            self.round_timer = 0
            self.round_number += 1
            if self.round_number > 10:
                self.round_number = 1
                self.wave_number += 1
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
            
            enemy = Enemy(x, y, self.tower_x, self.tower_y, self.wave_number, self.particle_group)
            log("WAVE", f"SPAWNING: {enemy}")
            enemies.add(enemy)
            log("WAVE", f"WAVEMANAGER RETURNING: {enemies}")
        return enemies
    