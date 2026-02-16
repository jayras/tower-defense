import pygame
import math
from typing import Optional
from testing import log

class EnemyProjectile(pygame.sprite.Sprite):
    """Projectile fired by ranged enemies at the tower."""
    
    def __init__(self, x: float, y: float, target_x: float, target_y: float, damage: float, owner, speed: float = 3.0):
        super().__init__()
        
        # Position
        self.x = x
        self.y = y
        
        # Target
        self.target_x = target_x
        self.target_y = target_y
        
        # Owner (the enemy that fired this)
        self.owner = owner
        
        # Stats
        self.damage = damage
        self.speed = speed
        
        # Visuals (red projectile to distinguish from tower projectiles)
        self.radius = 2
        self.color = (255, 100, 100)  # Light red
        
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        
        self.is_alive = True
        
        log("ENEMY_PROJECTILE", f"Enemy firing projectile at tower")
    
    def update(self, tower) -> None:
        """Move toward the tower."""
        if not self.is_alive:
            return
        
        # Check if owner is dead - if so, destroy this projectile
        if self.owner and getattr(self.owner, "dead", False):
            log("ENEMY_PROJECTILE", f"Owner died, destroying projectile")
            self.is_alive = False
            self.kill()
            return
            
        # Move toward target
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = math.hypot(dx, dy)
        
        if dist == 0:
            self.kill()
            return
        
        # Normalize and move
        dx /= dist
        dy /= dist
        self.x += dx * self.speed
        self.y += dy * self.speed
        
        # Check collision with tower (using tower radius)
        tower_dist = math.hypot(tower.x - self.x, tower.y - self.y)
        collision_dist = self.radius + tower.radius
        
        if tower_dist <= collision_dist:
            self.on_hit(tower)
    
    def on_hit(self, tower) -> None:
        """Deal damage to tower and destroy projectile."""
        if not self.is_alive:
            return
            
        tower.health -= self.damage
        log("ENEMY_PROJECTILE", f"Enemy projectile hit tower for {self.damage} damage")
        self.is_alive = False
        self.kill()
    
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the enemy projectile."""
        rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(self.image, rect)
