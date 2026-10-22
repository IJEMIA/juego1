import math
import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, poke_data):
        super().__init__()
        # Escalar el sprite descargado de la API
        self.image = pygame.transform.scale(poke_data["image"], (50, 50))
        self.rect = self.image.get_rect(center=(x, y))
        self.name = poke_data["name"]
        self.hp = poke_data["hp"]
        # Normalizar velocidad basada en stats de la API
        self.speed = max(1, poke_data["speed"] / 30)

    def update(self, player_pos):
        # Moverse hacia la posición del jugador
        px, py = player_pos
        dx, dy = px - self.rect.centerx, py - self.rect.centery
        dist = math.hypot(dx, dy)

        if dist != 0:
            self.rect.x += (dx / dist) * self.speed
            self.rect.y += (dy / dist) * self.speed
