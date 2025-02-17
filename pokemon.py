import requests
from io import BytesIO
import pygame
import random
import math

# Initialisation de Pygame (n'oublie pas d'appeler pygame.init() dans ton programme principal)
pygame.init()

class Pokemon:
    def __init__(self, name):
        self.name = name.lower()
        self.data = self._fetch_pokemon_data()
        self.types = self.data.get("types", [])
        self.stats = self.data.get("stats", {"hp": 100})  # Ajout d'un hp par défaut si non présent
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


class AttackEffect:
    """Classe pour gérer les effets visuels d'une attaque"""
    def __init__(self, attacker_name, attacker_types):
        self.attacker_name = attacker_name
        self.attacker_types = attacker_types
        self.duration = 30  # Durée totale de l'animation
        self.frame = 0
        
        # Déterminer le type d'effet
        if "fire" in attacker_types:
            self.effect_type = "fire"
            self.particles = [self._create_particle() for _ in range(20)]
        elif "electric" in attacker_types:
            self.effect_type = "electric"
        elif "water" in attacker_types:
            self.effect_type = "water"
        else:
            self.effect_type = "normal"
        
        # Couleur par défaut selon le type d'attaque
        self.color = (255, 0, 0)  # rouge pour l'effet normal
        if self.effect_type == "electric":
            self.color = (255, 255, 0)
        elif self.effect_type == "water":
            self.color = (0, 0, 255)
    
    def _create_particle(self):
        # Chaque particule aura une position relative, une vélocité, une taille et une durée de vie
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 5)
        return {
            "x": 0,
            "y": 0,
            "vx": math.cos(angle) * speed,
            "vy": math.sin(angle) * speed,
            "radius": random.randint(2, 5),
            "lifetime": random.randint(20, 30)
        }
    
    def draw(self, screen, x, y):
        center = (x + 50, y + 50)
        
        if self.effect_type == "fire":
            # Dessiner un effet de flamme avec particules
            for particle in self.particles:
                # Mettre à jour la position
                particle["x"] += particle["vx"]
                particle["y"] += particle["vy"]
                # Réduire la durée de vie
                particle["lifetime"] -= 1
                alpha = max(0, int(255 * (particle["lifetime"] / 30)))
                flame_color = (255, random.randint(100,150), 0, alpha)  # couleur orangée
                # Créer une surface pour la particule avec transparence
                surf = pygame.Surface((particle["radius"]*2, particle["radius"]*2), pygame.SRCALPHA)
                pygame.draw.circle(surf, flame_color, (particle["radius"], particle["radius"]), particle["radius"])
                screen.blit(surf, (center[0] + particle["x"] - particle["radius"], center[1] + particle["y"] - particle["radius"]))
                # Réinitialiser la particule si sa vie est terminée
                if particle["lifetime"] <= 0:
                    particle.update(self._create_particle())
            self.frame += 1
            if self.frame >= self.duration:
                self.frame = 0  # Réinitialiser pour boucler l'animation
        elif self.effect_type == "electric":
            # Effet d'éclair : dessiner des lignes animées autour du centre
            if self.frame < self.duration:
                for _ in range(3):
                    offset1 = (random.randint(-30, 30), random.randint(-30, 30))
                    offset2 = (random.randint(-30, 30), random.randint(-30, 30))
                    pygame.draw.line(screen, self.color, 
                                     (center[0] + offset1[0], center[1] + offset1[1]),
                                     (center[0] + offset2[0], center[1] + offset2[1]), 2)
                self.frame += 1
            else:
                self.frame = 0
        elif self.effect_type == "water":
            # Effet d'eau : dessiner des cercles bleutés qui se dilatent et s'estompent
            if self.frame < self.duration:
                radius = self.frame * 2
                alpha = max(0, 255 - int(255 * (self.frame / self.duration)))
                surf = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
                pygame.draw.circle(surf, (0, 0, 255, alpha), (radius, radius), radius, 2)
                screen.blit(surf, (center[0] - radius, center[1] - radius))
                self.frame += 1
            else:
                self.frame = 0
        else:
            # Effet normal : simple cercle rouge qui grandit
            if self.frame < self.duration:
                pygame.draw.circle(screen, self.color, center, self.frame * 2, 2)
                self.frame += 1
            else:
                self.frame = 0  # Réinitialiser après l'animation


class DefenseEffect:
    """Classe pour gérer les effets visuels de la défense"""
    def __init__(self, defender_name, defender_types):
        self.defender_name = defender_name
        self.defender_types = defender_types
        self.duration = 30  # Durée de l'animation de défense
        self.frame = 0
        self.active = True  # Pour appliquer l'effet de secousse
        self.base_color = (0, 255, 0)  # vert par défaut
        if "steel" in defender_types:
            self.base_color = (192, 192, 192)
        elif "psychic" in defender_types:
            self.base_color = (255, 0, 255)
    
    def draw(self, screen, x, y):
        center = (x + 50, y + 50)
        # Dessiner un bouclier circulaire pulsant autour du Pokémon
        if self.frame < self.duration:
            pulse = 5 * math.sin(self.frame / 3)
            radius = 60 + pulse
            alpha = max(0, 150 - int(150 * (self.frame / self.duration)))
            surf = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*self.base_color, alpha), (radius, radius), int(radius), 3)
            screen.blit(surf, (center[0] - radius, center[1] - radius))
            self.frame += 1
        else:
            self.frame = 0
            self.active = False  # L'effet se termine après la durée
