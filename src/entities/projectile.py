import math
import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 50, 50))  # Rojo Pokéball
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 8

        # Calcular ángulo y dirección hacia el mouse
        angle = math.atan2(target_y - y, target_x - x)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Destruir si sale de la pantalla
        if self.rect.right < 0 or self.rect.left > 800 or self.rect.bottom < 0 or self.rect.top > 600:
            self.kill()
