import pygame
import sys
import math
from game.settings import Settings
from game.tower import Tower
from game.wave import WaveManager
import testing

def main():
    settings = Settings()
    center_x = settings.get_window_width() // 2
    center_y = settings.get_window_height() // 2
    pygame.init()

    screen = pygame.display.set_mode((settings.get_window_width(), settings.get_window_height() ))
    pygame.display.set_caption("Tower Defense")

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    font = pygame.font.SysFont(None, 24)
    clock = pygame.time.Clock()
    FPS = 60

    tower = Tower(settings, center_x, center_y)
    enemies = pygame.sprite.Group()

    particles = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    wave_manager = WaveManager(settings, particles, center_x, center_y)
    
    testing.log("MAIN", f"Tower position: ({tower.x}, {tower.y})")

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
            # Debug: log first few enemy positions
            if dist < 200:
                testing.log("MAIN", f"Enemy close: pos=({enemy.x:.1f},{enemy.y:.1f}), tower=({tower.x},{tower.y}), dist={dist:.1f}")
            if dist < 60:
                testing.log("MAIN", f"ENEMY REACHED TOWER: dist={dist}, enemy.damage={enemy.damage}")
                tower.health -= enemy.damage
                testing.log("MAIN", f"TOWER HEALTH NOW: {tower.health}")
                enemy.kill()
                if tower.health <= 0:
                    testing.log("MAIN", "TOWER DESTROYED")
                    running = False

        # Spawn new enemies
        #new_enemies = wave_manager.update()
        #for enemy in new_enemies:
        #    enemies.add(enemy)
        for enemy in wave_manager.update():
            testing.log("MAIN", f"ADDING: {id(enemy)}")
            enemies.add(enemy)

        # Draw
        screen.fill(BLACK)
        tower.draw(screen)
        enemies.draw(screen)
        projectiles.draw(screen)
        particles.draw(screen)

        health_text = font.render(f"Tower Health: {tower.health}", True, WHITE)
        screen.blit(health_text, (10, 10))
        
        wave_text = font.render(f"Wave: {wave_manager.wave_number} Round: {wave_manager.round_number}", True, WHITE)
        screen.blit(wave_text, (10, 40))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

