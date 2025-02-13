import pygame
import random
from pokemon import Pokemon
from utils import draw_text

class Game:
    def __init__(self, screen, player_pokemon):
        self.screen = screen
        self.player_pokemon = player_pokemon
        self.opponent_pokemon = self._get_random_pokemon(player_pokemon.name)  # Passer le nom du Pokémon du joueur
        self.background = pygame.image.load("battle_pokemon.jpg")
        self.background = pygame.transform.scale(self.background, (800, 600))

    def _get_random_pokemon(self, excluded_pokemon_name):
        # Liste de quelques Pokémon pour l'exemple
        pokemon_list = ["pikachu", "bulbasaur", "charmander", "squirtle", "jigglypuff", "eevee", "snorlax", "mewtwo"]
        
        # Retirer le Pokémon choisi par le joueur de la liste des adversaires possibles
        pokemon_list = [p for p in pokemon_list if p != excluded_pokemon_name.lower()]
        
        if not pokemon_list:
            # Si la liste est vide (cas improbable), choisir un Pokémon par défaut
            return Pokemon("pikachu")
        
        random_pokemon_name = random.choice(pokemon_list)
        return Pokemon(random_pokemon_name)

    def run(self):
        running = True
        while running:
            self.screen.blit(self.background, (0, 0))
            draw_text(self.screen, f"Your Pokémon: {self.player_pokemon.name.capitalize()}", 50, 50)
            draw_text(self.screen, f"Opponent: {self.opponent_pokemon.name.capitalize()}", 50, 100)

            if self.player_pokemon.image:
                self.screen.blit(self.player_pokemon.image, (100, 200))
            if self.opponent_pokemon.image:
                self.screen.blit(self.opponent_pokemon.image, (500, 200))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False