import pygame
import math
import random
from game.projectile import Projectile

class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

        # Visuals
        self.radius = 50
        self.color = (0, 255, 0)
        self.active_projectiles = 0

        # Core stats
        self.range = 300
        self.health = 100

        # Offensive stats (upgradeable)
        self.damage = 10
        self.projectile_speed = 8
        self.crit_chance = 0.0
        self.crit_damage = 1.5
        self.pierce = 0
        self.splash_radius = 0

        # Multishot system (The Tower style)
        self.multishot_chance = 0.0      # % chance to fire multiple projectiles
        self.multishot_targets = 1       # how many targets if multishot triggers


    # ---------------------------------------------------------
    # Burst gating logic
    # ---------------------------------------------------------
    def can_fire(self):
        return self.active_projectiles == 0


    # ---------------------------------------------------------
    # Burst-based firing
    # ---------------------------------------------------------
    def shoot(self, enemies, projectiles):
        if not self.can_fire():
            return

        # -----------------------------------------------------
        # Step 1: Determine if multishot triggers
        # -----------------------------------------------------
        multishot_triggered = random.random() < self.multishot_chance
        burst_size = 1

        if multishot_triggered:
            burst_size = self.multishot_targets

        # -----------------------------------------------------
        # Step 2: Select targets
        # -----------------------------------------------------
        # Sort enemies by distance
        sorted_enemies = sorted(
            enemies,
            key=lambda e: math.hypot(e.x - self.x, e.y - self.y)
        )

        # Filter enemies within range
        valid_targets = [
            e for e in sorted_enemies
            if math.hypot(e.x - self.x, e.y - self.y) <= self.range
        ]

        if not valid_targets:
            return

        # Limit to burst size
        targets = valid_targets[:burst_size]

        # -----------------------------------------------------
        # Step 3: Fire projectiles
        # -----------------------------------------------------
        for target in targets:
            proj = Projectile(
                self.x,
                self.y,
                target,
                owner=self,
                damage=self.damage,
                speed=self.projectile_speed,
                crit_chance=self.crit_chance,
                crit_damage=self.crit_damage,
                pierce=self.pierce,
                splash_radius=self.splash_radius
            )
            projectiles.add(proj)
            self.active_projectiles += 1

    # ---------------------------------------------------------
    # Called by projectiles when they hit or expire
    # ---------------------------------------------------------
    def notify_projectile_resolved(self):
        self.active_projectiles -= 1
        if self.active_projectiles < 0:
            self.active_projectiles = 0  # safety

    # ---------------------------------------------------------
    # Draw tower + range
    # ---------------------------------------------------------
    def draw(self, screen):
        # Range circle
        pygame.draw.circle(screen, (128, 128, 128), (self.x, self.y), self.range, 1)

        # 12-sided tower
        points = []
        for i in range(12):
            angle = math.radians(i * 30)
            px = self.x + self.radius * math.cos(angle)
            py = self.y + self.radius * math.sin(angle)
            points.append((px, py))
        pygame.draw.polygon(screen, self.color, points, 1)

    def update(self):
        pass