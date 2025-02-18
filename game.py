import pygame
import random
import math
from pokemon import Pokemon
from utils import draw_text
from combat import Combat
from combat import Attack

class Game:
    def __init__(self, screen, player_pokemon):
        self.screen = screen
        self.player_pokemon = player_pokemon
        self.opponent_pokemon = self._get_random_pokemon(player_pokemon.name)
        self.background = pygame.image.load("battle_pokemon.jpg")
        self.background = pygame.transform.scale(self.background, (800, 600))

        # Agrandissement des sprites
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

        # Ajout des attaques possibles
        self.player_moves = [
            Attack("Charge", "normal", 40, 35),
            Attack("Flammèche", "fire", 40, 25),
            Attack("Pistolet à O", "water", 40, 25),
            Attack("Griffe", "normal", 50, 30)
        ]

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

            # Affichage des points de vie
            draw_text(self.screen, f"{self.player_pokemon.name.capitalize()} HP: {self.player_pokemon.stats['hp']}", 50, 150)
            draw_text(self.screen, f"{self.opponent_pokemon.name.capitalize()} HP: {self.opponent_pokemon.stats['hp']}", 50, 200)

            self.time += self.speed
            oscillation = math.sin(self.time) * self.amplitude

            player_x, player_y = 100, 300 + oscillation
            opponent_x, opponent_y = 550, 300 - oscillation

            # Dessiner les Pokémon avec leurs effets visuels
            self.player_pokemon.draw(self.screen, player_x, player_y)
            self.opponent_pokemon.draw(self.screen, opponent_x, opponent_y)

            if not self.game_over:
                if self.turn == self.player_pokemon:
                    self.display_attack_options()
                else:
                    self.opponent_attack()
                    self.turn = self.player_pokemon

            pygame.display.flip()
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if self.turn == self.player_pokemon:
                        if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                            attack_index = event.key - pygame.K_1
                            if 0 <= attack_index < len(self.player_moves):
                                self.player_attack(self.player_moves[attack_index])
                                self.turn = self.opponent_pokemon

            if self.player_pokemon.stats["hp"] <= 0 or self.opponent_pokemon.stats["hp"] <= 0:
                self.game_over = True
                winner = self.player_pokemon.name if self.opponent_pokemon.stats["hp"] <= 0 else self.opponent_pokemon.name
                draw_text(self.screen, f"{winner.capitalize()} wins!", 300, 300)
                pygame.display.flip()
                pygame.time.wait(3000)
                running = False

    def display_attack_options(self):
        """ Affichage des attaques disponibles avec leurs PP restants """
        for i, move in enumerate(self.player_moves):
            move_text = f"{i + 1}. {move.name} ({move.pp} PP)"
            draw_text(self.screen, move_text, 50, 450 + (i * 30))

    def player_attack(self, attack):
        """ Exécute une attaque du joueur """
        if attack.pp > 0:
            damage, effectiveness, critical, _ = self.combat.apply_damage(self.player_pokemon, self.opponent_pokemon, attack)
            attack.pp -= 1  # Réduction du PP

            draw_text(self.screen, f"{self.player_pokemon.name.capitalize()} used {attack.name}!", 50, 450)
            if critical:
                draw_text(self.screen, "🔥 Critical hit!", 50, 480)
            if effectiveness > 1:
                draw_text(self.screen, "It's super effective!", 50, 510)
            elif effectiveness < 1:
                draw_text(self.screen, "It's not very effective...", 50, 510)

    def opponent_attack(self):
        """ L'IA choisit une attaque aléatoire """
        move = random.choice(self.player_moves)
        damage, effectiveness, critical, _ = self.combat.apply_damage(self.opponent_pokemon, self.player_pokemon, move)

        draw_text(self.screen, f"{self.opponent_pokemon.name.capitalize()} used {move.name}!", 50, 450)
        if critical:
            draw_text(self.screen, "🔥 Critical hit!", 50, 480)
        if effectiveness > 1:
            draw_text(self.screen, "It's super effective!", 50, 510)
        elif effectiveness < 1:
            draw_text(self.screen, "It's not very effective...", 50, 510)
