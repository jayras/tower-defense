import pygame
import math
import random
from typing import Optional
from game.settings import Settings
from testing import log
from game.targetable import Targetable

class Projectile(pygame.sprite.Sprite):
    def __init__(self, settings: Settings, x: float, y: float, target: Targetable, owner):
        super().__init__()
        self.settings = settings

        # Position
        self.x = x
        self.y = y

        self.target: Optional[Targetable] = target
        self.owner = owner

        # Stats (from settings)
        self.pierce: int = self.settings.get_pierce()

        # Visuals
        self.radius = 3
        self.color = (255, 255, 0)

        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect: pygame.Rect = self.image.get_rect(center=(self.x, self.y))

        self.is_alive: bool = True

        log("PROJECTILE", f"CREATING PROJECTILE: {id(self)} targeting ENEMY: {id(self.target)}")

    # ---------------------------------------------------------
    # Update movement + collision
    # ---------------------------------------------------------
    def update(self, enemies: pygame.sprite.Group) -> None:
        # If target died or vanished, resolve projectile
        if not self.target or getattr(self.target, "dead", True):
            self.resolve()
            return

        # Move toward target
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = math.hypot(dx, dy)

        if dist == 0:
            self.resolve()
            return

        # Normalize
        dx /= dist
        dy /= dist

        # Move
        self.x += dx * self.settings.get_projectile_speed()
        self.y += dy * self.settings.get_projectile_speed()
        self.rect.center = (int(self.x), int(self.y))

        # Recalculate distance AFTER movement
        new_dist = math.hypot(self.target.x - self.x, self.target.y - self.y)

        # Collision check
        if self.rect.colliderect(self.target.rect):
            self.on_hit(enemies)
            return

    # ---------------------------------------------------------
    # Hit logic (crit, splash, pierce)
    # ---------------------------------------------------------
    def on_hit(self, enemies: pygame.sprite.Group) -> None:
        if not self.target or getattr(self.target, "dead", False):
            self.resolve()
            return
        
        # Crit calculation
        proj_dmg = self.settings.get_projectile_damage()

        # Splash damage: use the configured splash damage percentage
        splash_radius = self.settings.get_splash_radius()
        if splash_radius > 0:
            splash_dmg = self.settings.get_splash_damage()
            for e in enemies:
                if math.hypot(e.x - self.x, e.y - self.y) <= splash_radius:
                    e.take_damage(splash_dmg)
        else:
            self.target.take_damage(proj_dmg)

        # Pierce logic
        self.pierce -= 1
        if self.pierce <= 0:
            self.resolve()
            return

    # ---------------------------------------------------------
    # Cleanup + notify tower
    # ---------------------------------------------------------
    def resolve(self) -> None:
        self.target = None
        if not self.is_alive:
            return
        self.is_alive = False
        self.owner.notify_projectile_resolved()
        self.rect.center = (-9999, -9999)
        self.kill()
            
    # ---------------------------------------------------------
    # Draw
    # ---------------------------------------------------------
    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)
