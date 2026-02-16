import math
import pygame
from game.tower import Tower
from game.wave import WaveManager
from game.settings import Settings, GameSettings
from tests.test_config import test_config
import testing


class GameController:
    """Core game logic controller - handles all game state and updates."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        center_x = settings.get_window_width() // 2
        center_y = settings.get_window_height() // 2
        
        self.tower = Tower(settings, center_x, center_y)
        self.enemies = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.enemy_projectiles = pygame.sprite.Group()
        self.wave_manager = WaveManager(settings, self.particles, center_x, center_y, self.tower.range, self.enemy_projectiles)
        
        # Apply test config if enabled
        if test_config.enabled:
            if test_config.tower_health is not None:
                self.tower.health = test_config.tower_health
        
        self.game_over = False
        
        testing.log("CONTROLLER", f"Tower position: ({self.tower.x}, {self.tower.y})")
    
    def update(self):
        """Update all game entities and handle collisions."""
        if self.game_over:
            return
        
        # Tower firing
        self.tower.update()
        if self.tower.can_fire():
            self.tower.shoot(self.enemies, self.projectiles)
        
        # Update enemies with collision handling
        for enemy in self.enemies:
            enemy.update(self.enemies)
        
        # Update projectiles
        for proj in list(self.projectiles):
            proj.update(self.enemies)
        
        # Update enemy projectiles
        for enemy_proj in list(self.enemy_projectiles):
            enemy_proj.update(self.tower)
        
        # Update particles
        self.particles.update()
        
        # Enemy reaching tower
        for enemy in list(self.enemies):
            dist = math.hypot(enemy.x - self.tower.x, enemy.y - self.tower.y)
            reach_dist = self.tower.radius + enemy.radius + GameSettings.tower_contact_buffer
            if dist <= reach_dist:
                # Bounce enemy away from the tower on contact
                if dist == 0:
                    nx, ny = 1.0, 0.0
                else:
                    nx = (enemy.x - self.tower.x) / dist
                    ny = (enemy.y - self.tower.y) / dist
                
                testing.log("CONTROLLER", f"ENEMY REACHED TOWER: dist={dist}, enemy.damage={enemy.damage}")
                
                # Apply test config: invincible tower
                if not (test_config.enabled and test_config.invincible_tower):
                    self.tower.health -= enemy.damage
                    testing.log("CONTROLLER", f"TOWER HEALTH NOW: {self.tower.health}")
                else:
                    testing.log("CONTROLLER", "Tower is invincible (test mode)")
                
                # Move just outside the tower and push away
                enemy.x = self.tower.x + nx * (reach_dist + 1)
                enemy.y = self.tower.y + ny * (reach_dist + 1)
                bounce_speed = max(1.0, enemy.speed * 1.5)
                enemy.vx = nx * bounce_speed
                enemy.vy = ny * bounce_speed
                
                if self.tower.health <= 0:
                    testing.log("CONTROLLER", "TOWER DESTROYED")
                    self.game_over = True
                    return
        
        # Spawn new enemies
        for enemy in self.wave_manager.update():
            testing.log("CONTROLLER", f"ADDING: {enemy}")
            self.enemies.add(enemy)
    
    def is_game_over(self):
        """Check if the game is over."""
        return self.game_over
    
    def get_tower(self):
        """Get the tower instance."""
        return self.tower
    
    def get_enemies(self):
        """Get the enemies sprite group."""
        return self.enemies
    
    def get_projectiles(self):
        """Get the projectiles sprite group."""
        return self.projectiles
    
    def get_enemy_projectiles(self):
        """Get the enemy projectiles sprite group."""
        return self.enemy_projectiles
    
    def get_particles(self):
        """Get the particles sprite group."""
        return self.particles
    
    def get_wave_manager(self):
        """Get the wave manager."""
        return self.wave_manager
