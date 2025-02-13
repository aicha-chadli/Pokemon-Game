import pygame
import random
import math
from pokemon import Pokemon
from utils import draw_text

class Game:
    def __init__(self, screen, player_pokemon):
        self.screen = screen
        self.player_pokemon = player_pokemon
        self.opponent_pokemon = self._get_random_pokemon(player_pokemon.name)
        self.background = pygame.image.load("battle_pokemon.jpg")
        self.background = pygame.transform.scale(self.background, (800, 600))

        # Scaling factor to make Pokémon bigger
        self.scale_factor = 2

        # Resize Pokémon images
        self.player_pokemon.image = pygame.transform.scale(self.player_pokemon.image, 
                                                           (self.player_pokemon.image.get_width() * self.scale_factor, 
                                                            self.player_pokemon.image.get_height() * self.scale_factor))
        self.opponent_pokemon.image = pygame.transform.scale(self.opponent_pokemon.image, 
                                                            (self.opponent_pokemon.image.get_width() * self.scale_factor, 
                                                             self.opponent_pokemon.image.get_height() * self.scale_factor))

        # Timer pour l'oscillation
        self.time = 0
        self.amplitude = 10  # Amplitude de l'oscillation
        self.speed = 0.05  # Vitesse de l'oscillation

    def _get_random_pokemon(self, excluded_pokemon_name):
        pokemon_list = ["pikachu", "bulbasaur", "charmander", "squirtle", "jigglypuff", "eevee", "snorlax", "mewtwo"]
        pokemon_list = [p for p in pokemon_list if p != excluded_pokemon_name.lower()]
        
        if not pokemon_list:
            return Pokemon("pikachu")
        
        random_pokemon_name = random.choice(pokemon_list)
        return Pokemon(random_pokemon_name)

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            self.screen.blit(self.background, (0, 0))
            draw_text(self.screen, f"Your Pokémon: {self.player_pokemon.name.capitalize()}", 50, 50)
            draw_text(self.screen, f"Opponent: {self.opponent_pokemon.name.capitalize()}", 50, 100)

            # Calcul de l'oscillation
            self.time += self.speed
            oscillation = math.sin(self.time) * self.amplitude  # Valeur oscillante

            # Positions des Pokémon avec oscillation
            player_x, player_y = 100, 300 + oscillation
            opponent_x, opponent_y = 550, 300 - oscillation  # Oscille en opposition

            if self.player_pokemon.image:
                self.screen.blit(self.player_pokemon.image, (player_x, player_y))
            if self.opponent_pokemon.image:
                self.screen.blit(self.opponent_pokemon.image, (opponent_x, opponent_y))

            pygame.display.flip()
            clock.tick(60)  # 60 FPS

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
