import pygame
import random
import math
from pokemon import Pokemon
from utils import draw_text
from combat import Combat

class Game:
    def __init__(self, screen, player_pokemon):
        self.screen = screen
        self.player_pokemon = player_pokemon
        self.opponent_pokemon = self._get_random_pokemon(player_pokemon.name)
        self.background = pygame.image.load("battle_pokemon.jpg")
        self.background = pygame.transform.scale(self.background, (800, 600))
        self.scale_factor = 2
        self.player_pokemon.image = pygame.transform.scale(self.player_pokemon.image, 
                                                          (self.player_pokemon.image.get_width() * self.scale_factor, 
                                                           self.player_pokemon.image.get_height() * self.scale_factor))
        self.opponent_pokemon.image = pygame.transform.scale(self.opponent_pokemon.image, 
                                                             (self.opponent_pokemon.image.get_width() * self.scale_factor, 
                                                              self.opponent_pokemon.image.get_height() * self.scale_factor))
        self.time = 0
        self.amplitude = 10
        self.speed = 0.05
        self.combat = Combat(self.player_pokemon, self.opponent_pokemon)
        self.turn = self.player_pokemon if self.player_pokemon.stats["speed"] > self.opponent_pokemon.stats["speed"] else self.opponent_pokemon
        self.game_over = False

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

            self.time += self.speed
            oscillation = math.sin(self.time) * self.amplitude

            player_x, player_y = 100, 300 + oscillation
            opponent_x, opponent_y = 550, 300 - oscillation

            # Dessiner les Pokémon avec leurs effets visuels
            self.player_pokemon.draw(self.screen, player_x, player_y)
            self.opponent_pokemon.draw(self.screen, opponent_x, opponent_y)

            if not self.game_over:
                if self.turn == self.player_pokemon:
                    draw_text(self.screen, "1. Attack", 50, 500)
                    draw_text(self.screen, "2. Defend", 200, 500)
                else:
                    self.opponent_attack()
                    self.turn = self.player_pokemon

            pygame.display.flip()
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1 and self.turn == self.player_pokemon:
                        self.player_attack()
                        self.turn = self.opponent_pokemon
                    elif event.key == pygame.K_2 and self.turn == self.player_pokemon:
                        self.player_defend()
                        self.turn = self.opponent_pokemon

            if self.player_pokemon.stats["hp"] <= 0 or self.opponent_pokemon.stats["hp"] <= 0:
                self.game_over = True
                winner = self.player_pokemon.name if self.opponent_pokemon.stats["hp"] <= 0 else self.opponent_pokemon.name
                draw_text(self.screen, f"{winner.capitalize()} wins!", 300, 300)
                pygame.display.flip()
                pygame.time.wait(3000)
                running = False

    def player_attack(self):
        move = self.player_pokemon.get_random_move()
        damage = self.player_pokemon.attack(self.opponent_pokemon)  # Appel de la méthode attack
        draw_text(self.screen, f"{self.player_pokemon.name.capitalize()} used {move}!", 50, 450)
        draw_text(self.screen, f"{self.opponent_pokemon.name.capitalize()} took {damage} damage!", 50, 480)

    def player_defend(self):
        draw_text(self.screen, f"{self.player_pokemon.name.capitalize()} is defending!", 50, 450)

    def opponent_attack(self):
        move = self.opponent_pokemon.get_random_move()
        damage = self.opponent_pokemon.attack(self.player_pokemon)  # Appel de la méthode attack
        draw_text(self.screen, f"{self.opponent_pokemon.name.capitalize()} used {move}!", 50, 450)
        draw_text(self.screen, f"{self.player_pokemon.name.capitalize()} took {damage} damage!", 50, 480)