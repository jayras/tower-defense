import pygame
import sys
import math
from game.tower import Tower
from game.enemy import Enemy
from game.wave import WaveManager

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tower Defense")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Font for UI
font = pygame.font.SysFont(None, 24)

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Game objects
tower = Tower(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
wave_manager = WaveManager()

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    tower.update()
    if len(projectiles) == 0:
        tower.shoot(enemies, projectiles)
    enemies.update()
    projectiles.update()

    # Check collisions
    hits = pygame.sprite.groupcollide(projectiles, enemies, True, False)
    for proj, hit_enemies in hits.items():
        for enemy in hit_enemies:
            enemy.take_damage(proj.damage)
            if enemy.health <= 0:
                enemy.kill()

    # Check if enemies reach tower
    for enemy in enemies:
        dist = math.hypot(enemy.x - tower.x, enemy.y - tower.y)
        if dist < 60:  # Close enough to tower
            tower.health -= enemy.damage
            enemy.kill()  # Remove enemy after damaging
            if tower.health <= 0:
                running = False  # Game over

    # Spawn enemies
    new_enemies = wave_manager.update()
    for enemy in new_enemies:
        enemies.add(enemy)

    # Draw
    screen.fill(BLACK)
    tower.draw(screen)
    enemies.draw(screen)
    projectiles.draw(screen)

    # Draw UI
    health_text = font.render(f"Tower Health: {tower.health}", True, WHITE)
    screen.blit(health_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()