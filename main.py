import pygame
import sys
import math
from game.settings import GameSettings
from game.tower import Tower
from game.wave import WaveManager


def main():
    game_settings = GameSettings()
    center_x = game_settings.window_width // 2
    center_y = game_settings.window_height // 2
    pygame.init()

    screen = pygame.display.set_mode((game_settings.window_width, game_settings.window_height))
    pygame.display.set_caption("Tower Defense")

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    font = pygame.font.SysFont(None, 24)
    clock = pygame.time.Clock()
    FPS = 60

    tower = Tower(center_x, center_y)
    enemies = pygame.sprite.Group()

    particles = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    wave_manager = WaveManager(particles)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Tower firing (burst-gated)
        tower.update()
        if tower.can_fire():
            tower.shoot(enemies, projectiles)

        # Update enemies
        enemies.update()

        # Update projectiles (pass enemies list)
        for proj in list(projectiles):
            proj.update(enemies)

        # Update particles
        particles.update()  

        # Enemy reaching tower
        for enemy in list(enemies):
            dist = math.hypot(enemy.x - tower.x, enemy.y - tower.y)
            if dist < 60:
                tower.health -= enemy.damage
                enemy.kill()
                if tower.health <= 0:
                    running = False

        # Spawn new enemies
        #new_enemies = wave_manager.update()
        #for enemy in new_enemies:
        #    enemies.add(enemy)
        for enemy in wave_manager.update():
            print("ADDING:", id(enemy))
            enemies.add(enemy)

        # Draw
        screen.fill(BLACK)
        tower.draw(screen)
        enemies.draw(screen)
        projectiles.draw(screen)
        particles.draw(screen)

        health_text = font.render(f"Tower Health: {tower.health}", True, WHITE)
        screen.blit(health_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

