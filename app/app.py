import pygame
import sys
from game.settings import Settings
from app.scenes import MenuScene, GameScene
from tests.test_config import test_config


class GameApp:
    def __init__(self):
        self.settings = Settings()
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.settings.get_window_width(), self.settings.get_window_height())
        )
        pygame.display.set_caption("Tower Defense")
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.font = pygame.font.SysFont(None, 24)
        
        # Auto-start game if test mode is enabled
        if test_config.enabled and test_config.auto_start:
            self.scene = GameScene(self)
        else:
            self.scene = MenuScene(self)

    def change_scene(self, scene):
        self.scene = scene

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                self.scene.handle_event(event)

            if not running:
                break

            self.scene.update()
            self.scene.draw()
            pygame.display.flip()
            self.clock.tick(self.fps)

        pygame.quit()
        sys.exit()
