import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, target_enemy, speed=5):
        super().__init__()
        self.x = x
        self.y = y
        self.target = target_enemy  # Track the enemy object
        self.speed = speed
        self.radius = 1  # Very small projectile
        self.color = (255, 255, 0)  # Yellow for projectile
        self.damage = 5  # Damage dealt to enemies
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        # Check if target is still alive
        if not self.target or not self.target.alive():
            self.kill()
            return

        # Update target position
        target_x = self.target.x
        target_y = self.target.y

        # Move towards target
        import math
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)