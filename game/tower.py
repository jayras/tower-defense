import pygame
import math
import random
from typing import Optional
from game.projectile import Projectile
from game.settings import Settings
from tests.test_config import test_config
from game.targetable import Targetable

class Tower(pygame.sprite.Sprite):
    def __init__(self, settings: Settings, x: float, y: float):
        super().__init__()
        self.x = x
        self.y = y
        self.settings = settings

        # Visuals
        self.radius = 20
        self.color = (0, 255, 0)
        self.active_projectiles = 0

        # Health starts at max
        self.health = self.settings.get_tower_max_health()
        self.rect: pygame.Rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)


    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------
    @property
    def max_health(self) -> int:
        """Max health is dynamic and calculated from settings every time."""
        return self.settings.get_tower_max_health()

    @property
    def range(self) -> int:
        """Range is dynamic and calculated from settings every time."""
        base_range = self.settings.get_tower_range()
        
        # Apply test config: infinite range
        if test_config.enabled and test_config.infinite_range:
            return 999999  # Effectively infinite
        
        return base_range

    # ---------------------------------------------------------
    # Burst gating logic
    # ---------------------------------------------------------
    def can_fire(self) -> bool:
        return self.active_projectiles == 0


    # ---------------------------------------------------------
    # Burst-based firing
    # ---------------------------------------------------------
    def shoot(self, enemies: pygame.sprite.Group, projectiles: pygame.sprite.Group) -> None:
        if not self.can_fire():
            return

        # Determine burst size based on multishot trigger
        burst_size = 1
        if self.settings.get_multishot_triggered():
            burst_size = self.settings.get_multishot_targets()

        # Step 2: Select targets
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

        # Step 3: Fire projectiles
        for target in targets:
            proj = Projectile(
                self.settings,
                self.x,
                self.y,
                target,
                owner=self
            )
            projectiles.add(proj)
            self.active_projectiles += 1

    # ---------------------------------------------------------
    # Called by projectiles when they hit or expire
    # ---------------------------------------------------------
    def notify_projectile_resolved(self) -> None:
        self.active_projectiles -= 1
        if self.active_projectiles < 0:
            self.active_projectiles = 0  # safety

    # ---------------------------------------------------------
    # Draw tower + range
    # ---------------------------------------------------------
    def draw(self, screen: pygame.Surface) -> None:
        # Range circle - lighter and fuzzier with multiple semi-transparent circles
        range_surface = pygame.Surface((self.range * 2 + 10, self.range * 2 + 10), pygame.SRCALPHA)
        for i in range(3):
            alpha = 30 - (i * 8)  # Decreasing opacity
            color = (180, 180, 180, alpha)
            pygame.draw.circle(range_surface, color, (self.range + 5, self.range + 5), self.range - i, 1)
        screen.blit(range_surface, (self.x - self.range - 5, self.y - self.range - 5))

        # 6-sided tower (hexagon)
        points = []
        for i in range(6):
            angle = math.radians(i * 60)
            px = self.x + self.radius * math.cos(angle)
            py = self.y + self.radius * math.sin(angle)
            points.append((px, py))
        pygame.draw.polygon(screen, self.color, points, 1)

    def update(self) -> None:
        pass
    