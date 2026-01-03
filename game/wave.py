import pygame
from game.enemy import Enemy

class WaveManager:
    def __init__(self):
        self.wave_number = 0
        self.round_number = 0
        self.enemies_per_round = 5
        self.round_timer = 0
        self.round_delay = 2000  # 2 seconds between rounds
        self.screen_width = 1000
        self.screen_height = 700
        self.tower_x = self.screen_width // 2
        self.tower_y = self.screen_height // 2

    def update(self):
        self.round_timer += 16  # Approximate for 60 FPS
        if self.round_timer >= self.round_delay:
            self.round_timer = 0
            self.round_number += 1
            if self.round_number > 10:
                self.round_number = 1
                self.wave_number += 1
            return self.spawn_round()
        return []

    def spawn_round(self):
        enemies = []
        for _ in range(self.enemies_per_round):
            # Spawn from random edge
            side = pygame.time.get_ticks() % 4
            if side == 0:  # Top
                x = pygame.time.get_ticks() % self.screen_width
                y = 0
            elif side == 1:  # Right
                x = self.screen_width
                y = pygame.time.get_ticks() % self.screen_height
            elif side == 2:  # Bottom
                x = pygame.time.get_ticks() % self.screen_width
                y = self.screen_height
            else:  # Left
                x = 0
                y = pygame.time.get_ticks() % self.screen_height
            enemy = Enemy(x, y, self.tower_x, self.tower_y)
            enemies.append(enemy)
        return enemies