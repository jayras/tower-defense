import pygame
import math
import traceback
from game.death_particle import DeathParticle
from game.targetable import Targetable
from game.settings import GameSettings
from testing import log

class Enemy(pygame.sprite.Sprite, Targetable):
    # Base stats for this enemy type (can be overridden in subclasses)
    initial_health = 10
    initial_damage = 5  # Increased from 1 for visible scaling

    def __init__(self, x: float, y: float, target_x: float, target_y: float, wave_number: int, particle_group):
        super().__init__()
        self.x = x
        self.y = y
        self.particle_group = particle_group
        self.target_x = target_x
        self.target_y = target_y
        
        # Speed from GameSettings (static)
        self.speed = GameSettings.enemy_speed
        
        # Health and damage scale with wave number
        self.wave_number = wave_number
        self.health = self._calculate_health()
        self.damage = self._calculate_damage()
        
        self.size = 10  # Size of the square
        self.color = (255, 0, 0)  # Red for enemy
        self.radius = self.size / 2
        self.hit_timer = 0  # Timer for hit reaction
        self.dead = False
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.rect(self.image, self.color, (0, 0, self.size, self.size), 2)
        self.rect: pygame.Rect = self.image.get_rect(center=(self.x, self.y))
        log("ENEMY", f"CREATING ENEMY: {self}")

    # ---------------------------------------------------------
    # Scaling calculations based on wave number
    # ---------------------------------------------------------
    def _calculate_health(self) -> int:
        """Health scales with wave number."""
        base_health = self.initial_health
        # Simple scaling: health increases by 10% per wave
        scaling_factor = 1.0 + (self.wave_number * 0.1)
        return int(base_health * scaling_factor)

    def _calculate_damage(self) -> int:
        """Damage scales with wave number."""
        base_damage = self.initial_damage
        # Scaling: damage increases by 20% per wave
        scaling_factor = 1.0 + (self.wave_number * 0.2)
        return int(base_damage * scaling_factor)


    def update(self):
        if self.dead:
            log("ENEMY", f"WARNING: Dead enemy still updating: {self}")

        # Move towards tower
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed
        self.rect.center = (int(self.x), int(self.y))
        if self.hit_timer > 0:
            self.hit_timer -= 1

    def die(self):
        log("ENEMY", f"DIE CALLED ON: {id(self)}")

        if self.dead:
            log("ENEMY", "Enemy already dead, skipping die()")
            return
        self.dead = True

        # Bloom happens ONCE here
        if self.particle_group:
            for _ in range(20):
                log("ENEMY", f"Creating death particle at ({self.x}, {self.y})")
                particle = DeathParticle(self.x, self.y)
                self.particle_group.add(particle)

        self.kill()

    def take_damage(self, amount):
        log("ENEMY", f"TAKE_DAMAGE CALLED FOR: {id(self)} FROM: {traceback.format_stack()[-2]}")
        self.health -= amount
        self.hit_timer = 10  # Flash for 10 frames
        log("ENEMY", f"Enemy took {amount} damage, health now {self.health}")
        if self.health <= 0:
            log("ENEMY", "Enemy health depleted, calling die()")
            self.die()

    def draw(self, screen):
        if self.dead:
            log("ENEMY", f"WARNING: Dead enemy still drawing: {self}")

        # Change color if hit
        color = (255, 255, 255) if self.hit_timer > 0 else self.color
        # Redraw image with current color
        temp_image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.rect(temp_image, color, (0, 0, self.size, self.size), 1)
        screen.blit(temp_image, self.rect)