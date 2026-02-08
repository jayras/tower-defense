import math
import pygame
from game.tower import Tower
from game.wave import WaveManager
import testing


class Scene:
    def __init__(self, app):
        self.app = app

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        pass


class MenuScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        self.title = "Tower Defense"
        self.options = [
            "Enter - Start Game",
            "L - Lab",
            "O - Options",
            "R - Research",
            "Esc - Quit",
        ]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.app.change_scene(GameScene(self.app))
            elif event.key == pygame.K_l:
                self.app.change_scene(LabScene(self.app))
            elif event.key == pygame.K_o:
                self.app.change_scene(OptionsScene(self.app))
            elif event.key == pygame.K_r:
                self.app.change_scene(ResearchScene(self.app))
            elif event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    def draw(self):
        screen = self.app.screen
        screen.fill((10, 10, 10))
        font = self.app.font

        title_surf = font.render(self.title, True, (255, 255, 255))
        screen.blit(title_surf, (20, 20))

        for idx, line in enumerate(self.options):
            text_surf = font.render(line, True, (200, 200, 200))
            screen.blit(text_surf, (20, 60 + idx * 24))


class LabScene(Scene):
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.app.change_scene(MenuScene(self.app))

    def draw(self):
        screen = self.app.screen
        screen.fill((12, 12, 18))
        font = self.app.font
        text = font.render("Lab (placeholder) - Esc to return", True, (200, 200, 200))
        screen.blit(text, (20, 20))


class OptionsScene(Scene):
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.app.change_scene(MenuScene(self.app))

    def draw(self):
        screen = self.app.screen
        screen.fill((12, 18, 12))
        font = self.app.font
        text = font.render("Options (placeholder) - Esc to return", True, (200, 200, 200))
        screen.blit(text, (20, 20))


class ResearchScene(Scene):
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.app.change_scene(MenuScene(self.app))

    def draw(self):
        screen = self.app.screen
        screen.fill((18, 12, 12))
        font = self.app.font
        text = font.render("Research (placeholder) - Esc to return", True, (200, 200, 200))
        screen.blit(text, (20, 20))


class GameScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        settings = self.app.settings
        center_x = settings.get_window_width() // 2
        center_y = settings.get_window_height() // 2

        self.tower = Tower(settings, center_x, center_y)
        self.enemies = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.wave_manager = WaveManager(settings, self.particles, center_x, center_y)

        testing.log("MAIN", f"Tower position: ({self.tower.x}, {self.tower.y})")

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.app.change_scene(MenuScene(self.app))

    def update(self):
        self.tower.update()
        if self.tower.can_fire():
            self.tower.shoot(self.enemies, self.projectiles)

        for enemy in self.enemies:
            enemy.update(self.enemies)

        for proj in list(self.projectiles):
            proj.update(self.enemies)

        self.particles.update()

        for enemy in list(self.enemies):
            dist = math.hypot(enemy.x - self.tower.x, enemy.y - self.tower.y)
            if dist < 60:
                testing.log("MAIN", f"ENEMY REACHED TOWER: dist={dist}, enemy.damage={enemy.damage}")
                self.tower.health -= enemy.damage
                testing.log("MAIN", f"TOWER HEALTH NOW: {self.tower.health}")
                enemy.die()
                if self.tower.health <= 0:
                    testing.log("MAIN", "TOWER DESTROYED")
                    self.app.change_scene(MenuScene(self.app))
                    return

        for enemy in self.wave_manager.update():
            testing.log("MAIN", f"ADDING: {enemy}")
            self.enemies.add(enemy)

    def draw(self):
        screen = self.app.screen
        screen.fill((0, 0, 0))
        self.tower.draw(screen)

        for enemy in self.enemies:
            enemy.draw(screen)

        self.projectiles.draw(screen)
        self.particles.draw(screen)

        font = self.app.font
        health_text = font.render(f"Tower Health: {round(self.tower.health)}", True, (255, 255, 255))
        screen.blit(health_text, (10, 10))

        wave_text = font.render(
            f"Wave: {self.wave_manager.wave_number} Round: {self.wave_manager.round_number}",
            True,
            (255, 255, 255),
        )
        screen.blit(wave_text, (10, 40))
