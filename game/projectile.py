import pygame
import math
import random

class Projectile(pygame.sprite.Sprite):
    def __init__(
        self, x, y, target,
        owner,
        damage,
        speed,
        crit_chance,
        crit_damage,
        pierce,
        splash_radius
    ):
        super().__init__()

        # Position
        self.x = x
        self.y = y
        self.target = target
        self.owner = owner

        # Stats
        self.damage = damage
        self.speed = speed
        self.crit_chance = crit_chance
        self.crit_damage = crit_damage
        self.pierce = pierce
        self.splash_radius = splash_radius

        # Visuals
        self.radius = 3
        self.color = (255, 255, 0)

        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.alive = True

        print(f"CREATING PROJECTILE: {id(self)} targeting ENEMY: {id(self.target)}")

    # ---------------------------------------------------------
    # Update movement + collision
    # ---------------------------------------------------------
    def update(self, enemies):
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
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.rect.center = (self.x, self.y)

        # Recalculate distance AFTER movement
        new_dist = math.hypot(self.target.x - self.x, self.target.y - self.y)

        # Collision check
        if self.rect.colliderect(self.target.rect):
            self.on_hit(enemies)
            return

    # ---------------------------------------------------------
    # Hit logic (crit, splash, pierce)
    # ---------------------------------------------------------
    def on_hit(self, enemies):
        if getattr(self.target, "dead", False):
            self.resolve()
            return
        
        # Crit calculation
        dmg = self.damage
        if random.random() < self.crit_chance:
            dmg *= self.crit_damage

        # Splash damage
        if self.splash_radius > 0:
            for e in enemies:
                if math.hypot(e.x - self.x, e.y - self.y) <= self.splash_radius:
                    e.take_damage(dmg)
        else:
            self.target.take_damage(dmg)

        # Pierce logic
        self.pierce -= 1
        if self.pierce <= 0:
            self.resolve()
            return

    # ---------------------------------------------------------
    # Cleanup + notify tower
    # ---------------------------------------------------------
    def resolve(self):
        self.target = None
        if not self.alive:
            return
        self.alive = False
        self.owner.notify_projectile_resolved()
        self.rect.center = (-9999, -9999)
        self.kill()
            
    # ---------------------------------------------------------
    # Draw
    # ---------------------------------------------------------
    def draw(self, screen):
        screen.blit(self.image, self.rect)
