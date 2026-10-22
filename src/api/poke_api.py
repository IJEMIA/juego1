import io
import random
import requests
import pygame

class PokeAPI:
    BASE_URL = "https://pokeapi.co/api/v2/pokemon/"

    def __init__(self):
        self.cache = {}

    def get_random_pokemon(self, max_id=151):
        """Obtiene datos y la imagen de un Pokémon aleatorio (Primera Gen por defecto)."""
        pokemon_id = random.randint(1, max_id)
        
        # Verificar si ya está en caché
        if pokemon_id in self.cache:
            return self.cache[pokemon_id]

        url = f"{self.BASE_URL}{pokemon_id}"
        response = requests.get(url)
        
        if response.status_code != 200:
            return None

        data = response.json()
        image_url = data["sprites"]["front_default"]

        # Descargar la imagen del sprite
        img_response = requests.get(image_url)
        image_data = io.BytesIO(img_response.content)
        surface = pygame.image.load(image_data).convert_alpha()

        pokemon_data = {
            "id": pokemon_id,
            "name": data["name"].capitalize(),
            "hp": data["stats"][0]["base_stat"],
            "speed": data["stats"][5]["base_stat"],
            "image": surface
        }

        # Guardar en caché
        self.cache[pokemon_id] = pokemon_data
        return pokemon_data
