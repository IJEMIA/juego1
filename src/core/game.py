import random
import pygame
from src.api.poke_api import PokeAPI
from src.entities.player import Player
from src.entities.enemy import Enemy
from src.entities.projectile import Projectile
from src.ui.hud import HUD

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("PokéShooter: Legendary Catch")
        self.clock = pygame.time.Clock()
        self.running = True

        # API y Módulos
        self.api = PokeAPI()
        self.hud = HUD()

        # Grupos de Sprites
        self.all_sprites = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # Instanciar Jugador
        self.player = Player(400, 300)
        self.all_sprites.add(self.player)

        # Estado del Juego
        self.score = 0
        self.spawn_timer = 0

    def spawn_enemy(self):
        """Genera un enemigo Pokémon en un borde aleatorio usando la PokéAPI."""
        poke_data = self.api.get_random_pokemon()
        if not poke_data:
            return

        # Generar posición en los bordes de la pantalla
        edge = random.choice(["top", "bottom", "left", "right"])
        if edge == "top":
            x, y = random.randint(0, 800), -30
        elif edge == "bottom":
            x, y = random.randint(0, 800), 630
        elif edge == "left":
            x, y = -30, random.randint(0, 600)
        else:
            x, y = 830, random.randint(0, 600)

        enemy = Enemy(x, y, poke_data)
        self.enemies.add(enemy)
        self.all_sprites.add(enemy)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Disparar proyectil hacia el mouse
                mx, my = pygame.mouse.get_pos()
                bullet = Projectile(self.player.rect.centerx, self.player.rect.centery, mx, my)
                self.projectiles.add(bullet)
                self.all_sprites.add(bullet)

    def update(self):
        self.all_sprites.update()
        
        # Actualizar enemigos hacia la posición del jugador
        for enemy in self.enemies:
            enemy.update(self.player.rect.center)

        # Aparecer nuevos enemigos cada ~2 segundos
        self.spawn_timer += 1
        if self.spawn_timer >= 120:
            self.spawn_enemy()
            self.spawn_timer = 0

        # Colisión: Proyectil vs Enemigo
        hits = pygame.sprite.groupcollide(self.enemies, self.projectiles, False, True)
        for enemy, bullets in hits.items():
            enemy.hp -= 25  # Daño por disparo
            if enemy.hp <= 0:
                enemy.kill()
                self.score += 100

        # Colisión: Enemigo vs Jugador
        player_hits = pygame.sprite.spritecollide(self.player, self.enemies, True)
        for enemy in player_hits:
            self.player.health -= 15
            if self.player.health <= 0:
                self.running = False

    def draw(self):
        self.screen.fill((30, 30, 30))  # Fondo gris oscuro
        self.all_sprites.draw(self.screen)
        self.hud.draw(self.screen, self.player.health, self.score)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.draw()
        pygame.quit()
