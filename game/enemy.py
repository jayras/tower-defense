import pygame
import math
import traceback
from game.death_particle import DeathParticle
from game.targetable import Targetable
from game.settings import GameSettings
from testing import log
from game.enemy_stats import BasicStats
from game.enemy_names import EnemyNames


class Enemy(pygame.sprite.Sprite, Targetable):
    # Base stats for this enemy type (can be overridden in subclasses)
    initial_health = 10
    initial_damage = 5  # Increased from 1 for visible scaling

    def __init__(self, x: float, y: float, target_x: float, target_y: float, wave_number: int, particle_group):
        super().__init__()
        self.name = EnemyNames.get_name()
        self.x = x
        self.y = y
        self.particle_group = particle_group
        self.target_x = target_x
        self.target_y = target_y
        
        # Health and damage scale with wave number
        self.wave_number = wave_number
        self.health = BasicStats.health(wave_number)
        self.damage = BasicStats.attack(wave_number)
        # Base speed by enemy type and wave, scaled by overall game speed.
        self.speed = BasicStats.speed(wave_number) * GameSettings.game_speed
        self.mass = BasicStats.mass(wave_number)

        self.size = 10  # Size of the square
        self.color = (255, 0, 0)  # Red for enemy
        self.radius = self.size / 2
        self.hit_timer = 0  # Timer for hit reaction
        self.dead = False
        
        # Physics properties
        self.vx = 0.0  # Velocity from collisions
        self.vy = 0.0
        self.rotation = 0.0  # Rotation angle in degrees
        self.angular_velocity = 0.0  # Rotation speed
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.rect(self.image, self.color, (0, 0, self.size, self.size), 2)
        self.rect: pygame.Rect = self.image.get_rect(center=(self.x, self.y))
        log("ENEMY", f"CREATING ENEMY: {self}")

    def __str__(self):
        return self.name


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


    def update(self, enemies=None):
        if self.dead:
            log("ENEMY", f"WARNING: Dead enemy still updating: {self}")

        # Move towards tower
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed
        
        # Apply physics velocity (from collisions)
        self.x += self.vx
        self.y += self.vy
        
        # Apply rotation
        self.rotation += self.angular_velocity
        
        # Damping
        self.vx *= 0.9
        self.vy *= 0.9
        self.angular_velocity *= 0.95
        
        # Handle collisions with other enemies
        if enemies:
            self.handle_collisions(enemies)
        
        self.rect.center = (int(self.x), int(self.y))
        if self.hit_timer > 0:
            self.hit_timer -= 1

    def die(self):
        log("ENEMY", f"DIE CALLED ON: {self}")

        if self.dead:
            log("ENEMY", "Enemy already dead, skipping die()")
            return
        self.dead = True

        # Bloom happens ONCE here
        if self.particle_group is not None:
            for _ in range(20):
                particle = DeathParticle(self.x, self.y)
                self.particle_group.add(particle)

        self.kill()

    def handle_collisions(self, enemies):
        """Handle physics collisions with other enemies."""
        for other in enemies:
            if other is self or other.dead:
                continue
            
            # Check collision
            dx = other.x - self.x
            dy = other.y - self.y
            dist = math.hypot(dx, dy)
            min_dist = self.radius + other.radius
            
            if dist < min_dist and dist > 0:
                # Collision detected - calculate response
                overlap = min_dist - dist
                
                # Normalize collision vector
                nx = dx / dist
                ny = dy / dist
                
                # Mass ratio for impulse calculation
                total_mass = self.mass + other.mass
                self_ratio = other.mass / total_mass
                other_ratio = self.mass / total_mass
                
                # Separate enemies based on mass
                push_strength = overlap * 0.5
                self.x -= nx * push_strength * self_ratio
                self.y -= ny * push_strength * self_ratio
                other.x += nx * push_strength * other_ratio
                other.y += ny * push_strength * other_ratio
                
                # Apply velocity impulse
                impulse = 0.3
                self.vx -= nx * impulse * self_ratio
                self.vy -= ny * impulse * self_ratio
                other.vx += nx * impulse * other_ratio
                other.vy += ny * impulse * other_ratio
                
                # Calculate torque for rotation (perpendicular to collision)
                # Torque direction depends on collision offset from center
                torque = (nx * self.vy - ny * self.vx) * 0.5
                self.angular_velocity += torque / self.mass
                other.angular_velocity -= torque / other.mass

    def take_damage(self, amount):
        log("ENEMY", f"TAKE_DAMAGE CALLED ON: {self} FOR AMOUNT: {amount}   CURRENT HEALTH: {self.health}")
        self.health -= amount
        self.hit_timer = 10  # Flash for 10 frames
        if self.health <= 0:
            log("ENEMY", "Enemy health depleted, calling die()")
            self.die()

    def draw(self, screen):
        if self.dead:
            log("ENEMY", f"WARNING: Dead enemy still drawing: {self}")

        # Change color if hit
        color = (255, 255, 255) if self.hit_timer > 0 else self.color
        
        # Create rotated square
        temp_image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.rect(temp_image, color, (0, 0, self.size, self.size), 1)
        
        # Rotate the image
        rotated_image = pygame.transform.rotate(temp_image, self.rotation)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        
        screen.blit(rotated_image, rotated_rect)