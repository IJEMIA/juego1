import pygame

class HUD:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 20, bold=True)

    def draw(self, surface, health, score):
        # Dibujar Puntuación
        score_text = self.font.render(f"Puntos: {score}", True, (255, 255, 255))
        surface.blit(score_text, (20, 20))

        # Dibujar Barra de Vida
        pygame.draw.rect(surface, (100, 100, 100), (20, 50, 200, 20))
        if health > 0:
            pygame.draw.rect(surface, (0, 255, 0), (20, 50, health * 2, 20))
        pygame.draw.rect(surface, (255, 255, 255), (20, 50, 200, 20), 2)
