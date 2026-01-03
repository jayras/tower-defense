import pygame
import math
from game.projectile import Projectile

class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.radius = 50
        self.color = (0, 255, 0)  # Green for tower
        self.range = 300  # 30 meters * 10px/m
        self.multi_fire = 1  # number of projectiles per shot
        self.health = 100  # Tower health

    def update(self):
        # Tower logic here
        pass

    def shoot(self, enemies, projectiles):
        # Find closest enemy within range
        closest_enemy = None
        min_dist = float('inf')
        for enemy in enemies:
            dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
            if dist <= self.range and dist < min_dist:
                min_dist = dist
                closest_enemy = enemy
        if closest_enemy:
            for _ in range(self.multi_fire):
                proj = Projectile(self.x, self.y, closest_enemy)
                projectiles.add(proj)

    def draw(self, screen):
        # Draw range circle
        pygame.draw.circle(screen, (128, 128, 128), (self.x, self.y), self.range, 1)
        # Draw tower
        points = []
        for i in range(12):
            angle = math.radians(i * 30)  # 360/12 = 30 degrees
            px = self.x + self.radius * math.cos(angle)
            py = self.y + self.radius * math.sin(angle)
            points.append((px, py))
        pygame.draw.polygon(screen, self.color, points, 1)