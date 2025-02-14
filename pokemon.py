import requests
from io import BytesIO
import pygame
import random

class Pokemon:
    def __init__(self, name):
        self.name = name.lower()
        self.data = self._fetch_pokemon_data()
        self.types = self.data.get("types", [])
        self.stats = self.data.get("stats", {})
        self.image = self._load_image()
        self.moves = self._fetch_pokemon_moves()
        
        # Attributs pour les effets visuels
        self.attack_effect = None
        self.defense_effect = None

    def _fetch_pokemon_data(self):
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.name}")
        if response.status_code == 200:
            data = response.json()           
            return {
                "id": data["id"],
                "name": data["name"],
                "types": [t["type"]["name"] for t in data["types"]],
                "stats": {s["stat"]["name"]: s["base_stat"] for s in data["stats"]},
            }
        return {}

    def _fetch_pokemon_moves(self):
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.name}")
        if response.status_code == 200:
            data = response.json()
            moves = [move["move"]["name"] for move in data["moves"]]
            return moves
        return []

    def _load_image(self):
        if "id" in self.data:
            response = requests.get(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{self.data['id']}.png")
            if response.status_code == 200:
                image = pygame.image.load(BytesIO(response.content))
                return pygame.transform.scale(image, (100, 100))
        return None

    def get_random_move(self):
        if self.moves:
            return random.choice(self.moves)
        return "tackle"  # Fallback move

    def attack(self, target):
        """Attaque le Pokémon cible et déclenche l'effet visuel"""
        damage = random.randint(10, 30)  # Dégât aléatoire de l'attaque
        target.stats["hp"] -= damage  # Mise à jour des points de vie de la cible
        self.attack_effect = AttackEffect(self.name, self.types)  # Créer l'effet d'attaque
        target.defense_effect = DefenseEffect(target.name, target.types)  # Créer l'effet de défense
        return damage

    def draw(self, screen, x, y):
        """Dessiner l'image du Pokémon"""
        if self.image:
            screen.blit(self.image, (x, y))
        if self.attack_effect:
            self.attack_effect.draw(screen, x, y)
        if self.defense_effect:
            self.defense_effect.draw(screen, x, y)

    @staticmethod
    def get_pokemon_names(limit=151):
        url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}"
        response = requests.get(url)
        pokemon_names = []
        
        if response.status_code == 200:
            data = response.json()
            for pokemon in data['results']:
                pokemon_names.append(pokemon['name'])
        
        return pokemon_names


class AttackEffect:
    """Classe pour gérer les effets visuels d'une attaque"""
    def __init__(self, attacker_name, attacker_types):
        self.attacker_name = attacker_name
        self.attacker_types = attacker_types
        self.duration = 30  # Durée de l'animation de l'attaque
        self.frames = 0
        self.color = (255, 0, 0)  # Par défaut, un effet de feu (rouge)

        # Personnaliser les effets selon le type du Pokémon
        if "electric" in attacker_types:
            self.color = (255, 255, 0)  # Jaune pour un type électrique
        elif "water" in attacker_types:
            self.color = (0, 0, 255)  # Bleu pour un type eau

    def draw(self, screen, x, y):
        """Dessiner l'effet d'attaque"""
        if self.frames < self.duration:
            pygame.draw.circle(screen, self.color, (x + 50, y + 50), self.frames * 2)
            self.frames += 1
        else:
            self.frames = 0  # Réinitialiser après la fin de l'animation


class DefenseEffect:
    """Classe pour gérer les effets visuels de la défense"""
    def __init__(self, defender_name, defender_types):
        self.defender_name = defender_name
        self.defender_types = defender_types
        self.duration = 30  # Durée de l'animation de défense
        self.frames = 0
        self.color = (0, 255, 0)  # Par défaut, un effet de défense (vert)

        # Personnaliser les effets selon le type du Pokémon
        if "steel" in defender_types:
            self.color = (192, 192, 192)  # Gris métallique pour un type acier
        elif "psychic" in defender_types:
            self.color = (255, 0, 255)  # Violet pour un type psychique

    def draw(self, screen, x, y):
        """Dessiner l'effet de défense"""
        if self.frames < self.duration:
            pygame.draw.line(screen, self.color, (x + 50, y + 50), (x + 100, y + 50), 5)
            self.frames += 1
        else:
            self.frames = 0  # Réinitialiser après la fin de l'animation