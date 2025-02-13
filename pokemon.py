import requests
from io import BytesIO
import pygame

class Pokemon:
    def __init__(self, name):
        self.name = name.lower()
        self.data = self._fetch_pokemon_data()
        self.types = self.data.get("types", [])
        self.stats = self.data.get("stats", {})
        self.image = self._load_image()

    def _fetch_pokemon_data(self):
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.name}")
        if response.status_code == 200:
            data = response.json()
            return {
                "id": data["id"],  # On récupère l'ID
                "types": [t["type"]["name"] for t in data["types"]],
                "stats": {s["stat"]["name"]: s["base_stat"] for s in data["stats"]},
            }
        return {}

    def _load_image(self):
        if "id" in self.data:
            response = requests.get(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{self.data['id']}.png")
            if response.status_code == 200:
                image = pygame.image.load(BytesIO(response.content))
                return pygame.transform.scale(image, (100, 100))
        return None

