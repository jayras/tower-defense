import pygame
import math
from game.enemy import Enemy
from game.enemy_projectile import EnemyProjectile
from game.enemy_type import EnemyType, RangedEnemy as RangedEnemyType
from game.enemy_stats import EnemyStats
from testing import log


class RangedEnemy(Enemy):
    """Ranged enemy that stops at tower range and shoots projectiles."""
    
    def __init__(self, x: float, y: float, target_x: float, target_y: float, wave_number: int, 
                 type: EnemyType, stats: EnemyStats, particle_group, tower_range: int, 
                 enemy_projectiles: pygame.sprite.Group):
        # Call parent constructor
        super().__init__(x, y, target_x, target_y, wave_number, type, stats, particle_group)
        
        # Ranged-specific properties
        self.tower_range = tower_range  # Tower's range in pixels
        self.enemy_projectiles = enemy_projectiles
        self.shooting_cooldown = 0  # Frames until can shoot again
        self.shooting_rate = 60  # Shoot every 60 frames (1 second at 60fps)
        self.at_shooting_position = False
        self.my_projectiles = []  # Track projectiles created by this enemy
        
    def update(self, enemies=None):
        """Override update to handle ranged enemy behavior."""
        if self.dead:
            log("ENEMY", f"WARNING: Dead enemy still updating: {self}")
            return
        
        # Calculate distance to tower
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = math.hypot(dx, dy)
        
        # Target position: just inside tower range (90% of range)
        target_dist = self.tower_range * 0.9
        
        if dist > target_dist + 5:  # +5 pixel buffer
            # Move toward range ring
            if dist > 0:
                self.x += (dx / dist) * self.speed
                self.y += (dy / dist) * self.speed
            self.at_shooting_position = False
        else:
            # At shooting position, stop moving and shoot
            self.at_shooting_position = True
            self.shoot_at_tower()
        
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
        
        # Update timers
        if self.hit_timer > 0:
            self.hit_timer -= 1
        if self.shooting_cooldown > 0:
            self.shooting_cooldown -= 1
    
    def shoot_at_tower(self):
        """Shoot a projectile at the tower."""
        if not self.at_shooting_position:
            return
            
        if self.shooting_cooldown <= 0:
            # Create enemy projectile
            projectile = EnemyProjectile(
                self.x, self.y,
                self.target_x, self.target_y,
                self.damage,
                owner=self,
                speed=3.0
            )
            self.enemy_projectiles.add(projectile)
            self.my_projectiles.append(projectile)
            self.shooting_cooldown = self.shooting_rate
            log("ENEMY", f"{self.name} shooting at tower!")
    
    def die(self):
        """Override die to destroy all projectiles created by this enemy."""
        # Destroy all projectiles fired by this enemy
        for proj in self.my_projectiles:
            if proj.is_alive:
                log("ENEMY", f"Destroying projectile from dead enemy {self.name}")
                proj.is_alive = False
                proj.kill()
        self.my_projectiles.clear()
        
        # Call parent die
        super().die()
