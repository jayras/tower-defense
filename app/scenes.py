import math
import pygame
from game.game_controller import GameController
import testing
from game.settings import GameSettings


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
        self.controller = GameController(self.app.settings)

    def abbreviate_number(self, num):
        """Abbreviate large numbers with K, M, B suffixes."""
        if num >= 1_000_000_000:
            return f"{num / 1_000_000_000:.2f}B"
        elif num >= 1_000_000:
            return f"{num / 1_000_000:.2f}M"
        elif num >= 1_000:
            return f"{num / 1_000:.2f}K"
        else:
            return f"{num:.2f}"

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.app.change_scene(MenuScene(self.app))

    def update(self):
        self.controller.update()
        
        # Check for game over
        if self.controller.is_game_over():
            self.app.change_scene(MenuScene(self.app))

    def draw(self):
        screen = self.app.screen
        screen.fill((0, 0, 0))
        
        # Get game state from controller
        tower = self.controller.get_tower()
        enemies = self.controller.get_enemies()
        projectiles = self.controller.get_projectiles()
        enemy_projectiles = self.controller.get_enemy_projectiles()
        particles = self.controller.get_particles()
        wave_manager = self.controller.get_wave_manager()
        
        # Draw game entities
        tower.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        for projectile in projectiles:
            projectile.draw(screen)
        for enemy_proj in enemy_projectiles:
            enemy_proj.draw(screen)
        particles.draw(screen)

        font = self.app.font
        
        # --- Upper Left: Tower Health Bar ---
        bar_width = 250
        bar_height = 30
        bar_x = 10
        bar_y = 10
        
        # Background of bar
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        
        # Health fill
        health_pct = max(0, min(1, tower.health / tower.max_health))
        fill_width = int(bar_width * health_pct)
        health_color = (0, 255, 0) if health_pct > 0.5 else (255, 255, 0) if health_pct > 0.25 else (255, 0, 0)
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, fill_width, bar_height))
        
        # Border
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Text in the middle
        health_text = f"{self.abbreviate_number(tower.health)} / {self.abbreviate_number(tower.max_health)}"
        text_surf = font.render(health_text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(bar_x + bar_width // 2, bar_y + bar_height // 2))
        screen.blit(text_surf, text_rect)
        
        # --- Upper Right: Enemy Stats & Wave Info ---
        right_x = self.app.settings.get_window_width() - 10
        
        # Wave number
        wave_text = font.render(f"Wave: {wave_manager.wave_number}", True, (255, 255, 255))
        wave_rect = wave_text.get_rect(topright=(right_x, 10))
        screen.blit(wave_text, wave_rect)
        
        # Round progress bar (10 rounds per wave)
        round_bar_width = 250
        round_bar_height = 20
        round_bar_x = right_x - round_bar_width
        round_bar_y = wave_rect.bottom + 5
        
        # Background
        pygame.draw.rect(screen, (50, 50, 50), (round_bar_x, round_bar_y, round_bar_width, round_bar_height))
        
        # Progress fill
        rounds_total = 10
        round_pct = (wave_manager.round_number - 1) / rounds_total if wave_manager.round_number > 0 else 0
        round_fill_width = int(round_bar_width * round_pct)
        pygame.draw.rect(screen, (100, 150, 255), (round_bar_x, round_bar_y, round_fill_width, round_bar_height))
        
        # Border
        pygame.draw.rect(screen, (255, 255, 255), (round_bar_x, round_bar_y, round_bar_width, round_bar_height), 2)
        
        # Enemy stats (show first enemy's stats as reference)
        if len(enemies) > 0:
            sample_enemy = list(enemies)[0]
            enemy_health_text = font.render(f"Enemy HP: {self.abbreviate_number(sample_enemy.health)}", True, (255, 100, 100))
            enemy_health_rect = enemy_health_text.get_rect(topright=(right_x, round_bar_y + round_bar_height + 10))
            screen.blit(enemy_health_text, enemy_health_rect)
            
            enemy_attack_text = font.render(f"Enemy ATK: {self.abbreviate_number(sample_enemy.damage)}", True, (255, 150, 100))
            enemy_attack_rect = enemy_attack_text.get_rect(topright=(right_x, enemy_health_rect.bottom + 5))
            screen.blit(enemy_attack_text, enemy_attack_rect)
