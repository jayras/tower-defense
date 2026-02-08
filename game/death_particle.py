import pygame
import math
import random

class DeathParticle(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float):
        super().__init__()

        self.x = x
        self.y = y

        # Random outward direction
        angle = random.uniform(0, math.tau)
        self.dx = math.cos(angle) * random.uniform(2, 4)
        self.dy = math.sin(angle) * random.uniform(2, 4)

        # Visuals
        self.radius = 2
        self.color = (255, 255, 0)

        self.life = random.randint(4, 6)  # frames

        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))

    def update(self) -> None:
        # Move outward
        self.x += self.dx
        self.y += self.dy
        self.rect.center = (int(self.x), int(self.y))

        # Shrink or fade
        self.life -= 1
        if self.life <= 0:
            self.kill()
