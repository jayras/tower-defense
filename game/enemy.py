import pygame
import math

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, speed=2):
        super().__init__()
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.speed = speed
        self.size = 10  # Size of the square
        self.color = (255, 0, 0)  # Red for enemy
        self.health = 10  # Enemy health
        self.damage = 1  # Damage dealt to tower
        self.hit_timer = 0  # Timer for hit reaction
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.rect(self.image, self.color, (0, 0, self.size, self.size), 1)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        # Move towards tower
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed
        self.rect.center = (self.x, self.y)
        if self.hit_timer > 0:
            self.hit_timer -= 1

    def take_damage(self, amount):
        self.health -= amount
        self.hit_timer = 10  # Flash for 10 frames

    def draw(self, screen):
        # Change color if hit
        color = (255, 255, 255) if self.hit_timer > 0 else self.color
        # Redraw image with current color
        temp_image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.rect(temp_image, color, (0, 0, self.size, self.size), 1)
        screen.blit(temp_image, self.rect)