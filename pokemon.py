import requests
from io import BytesIO
import pygame
import random
import math


# Initialisation de Pygame (n'oublie pas d'appeler pygame.init() dans ton programme principal)
pygame.init()

class Pokemon:
    def __init__(self, name, level=1):
        self.name = name.lower()
        self.level = level  # Added level attribute with a default value of 1
        self.data = self._fetch_pokemon_data()
        self.types = self.data.get("types", [])
        self.stats = self.data.get("stats", {"hp": 100})  # Default HP if not present
        self.image = self._load_image()
        self.moves = self._fetch_pokemon_moves()
        
        # Attributs pour les effets visuels
        self.attack_effect = None
        self.defense_effect = None
        self.damage_text = None
        self.damage_timer = 0
        self.damage_pos = None

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
            moves = [move["move"]["name"] for move in data.get("moves", [])]
            return moves
        return []


    def _load_image(self):
        if "id" in self.data:
            response = requests.get(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{self.data['id']}.png")
            if response.status_code == 200:
                image = pygame.image.load(BytesIO(response.content)).convert_alpha()
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
        
        # Création d'effets visuels selon le type
        self.attack_effect = AttackEffect(self.name, self.types)
        target.defense_effect = DefenseEffect(target.name, target.types)
        return damage

    def draw(self, screen, x, y):
        """Dessiner l'image du Pokémon avec un léger effet de secousse en cas de défense active"""
        draw_x, draw_y = x, y
        # Si un effet de défense est actif, on applique un petit décalage (secousse)
        if self.defense_effect and self.defense_effect.active:
            offset = 5
            draw_x += random.randint(-offset, offset)
            draw_y += random.randint(-offset, offset)

        if self.image:
            screen.blit(self.image, (draw_x, draw_y))

        # Mostrar el texto de daño si existe
        if self.damage_text and self.damage_timer > 0:
            font = pygame.font.Font('Consolab.ttf', 26)
            text = font.render(f"-{self.damage_text}", True, (255, 0, 0))  # Texto rojo
            # Posición del texto: encima de la cabeza del pokémon
            if not self.damage_pos:
                self.damage_pos = [draw_x + self.image.get_width() // 2, draw_y - 20]
            # Hacer que el texto suba y se desvanezca
            self.damage_pos[1] -= 0.3  # Mover hacia arriba
            alpha = int(255 * (self.damage_timer / 60))  # Desvanecer gradualmente
            text.set_alpha(alpha)
            text_rect = text.get_rect(center=(self.damage_pos[0], self.damage_pos[1]))
            screen.blit(text, text_rect)
            self.damage_timer -= 1
            if self.damage_timer <= 0:
                self.damage_text = None
                self.damage_pos = None

        # Dessiner les effets d'attaque et de défense par-dessus
        if self.attack_effect:
            self.attack_effect.draw(screen, draw_x, draw_y)
        if self.defense_effect:
            self.defense_effect.draw(screen, draw_x, draw_y)

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


