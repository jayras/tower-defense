import pygame
import math
import traceback
from game.death_particle import DeathParticle

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, speed, particle_group):
        super().__init__()
        self.x = x
        self.y = y
        self.particle_group = particle_group
        self.target_x = target_x
        self.target_y = target_y
        self.speed = speed
        self.size = 10  # Size of the square
        self.color = (255, 0, 0)  # Red for enemy
        self.radius = self.size / 2
        self.health = 10  # Enemy health
        self.damage = 1  # Damage dealt to tower
        self.hit_timer = 0  # Timer for hit reaction
        self.dead = False
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.rect(self.image, self.color, (0, 0, self.size, self.size), 2)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        print("CREATING ENEMY:", self)


    def update(self):
        if self.dead:
            print("WARNING: Dead enemy still updating:", self)

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

    def die(self):
        print("DIE CALLED ON:", id(self))

        if self.dead:
            print("Enemy already dead, skipping die()")
            return
        self.dead = True

        # Bloom happens ONCE here
        if self.particle_group:
            for _ in range(20):
                print("Creating death particle at ({}, {})".format(self.x, self.y))
                particle = DeathParticle(self.x, self.y)
                self.particle_group.add(particle)

        self.kill()

    def take_damage(self, amount):
        print("TAKE_DAMAGE CALLED FOR:", id(self), "FROM:", traceback.format_stack()[-2])
        self.health -= amount
        self.hit_timer = 10  # Flash for 10 frames
        print("Enemy took {} damage, health now {}".format(amount, self.health))
        if self.health <= 0:
            print("Enemy health depleted, calling die()")
            self.die()

    def draw(self, screen):
        if self.dead:
            print("WARNING: Dead enemy still drawing:", self)

        # Change color if hit
        color = (255, 255, 255) if self.hit_timer > 0 else self.color
        # Redraw image with current color
        temp_image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.rect(temp_image, color, (0, 0, self.size, self.size), 1)
        screen.blit(temp_image, self.rect)