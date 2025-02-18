import pygame
import random
import math
from pokemon import Pokemon
from utils import draw_text
from combat import Combat
from combat import Attack
from save_manager import SaveManager

class Game:
    def __init__(self, screen, player_pokemon, opponent_pokemon=None):
        self.screen = screen
        self.player_pokemon = player_pokemon
        # Si se proporciona un oponente específico, usarlo, sino elegir uno aleatorio
        self.opponent_pokemon = opponent_pokemon if opponent_pokemon else self._get_random_pokemon(player_pokemon.name)
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

    def add_message(self, message):
        """Ajoute un message au log et conserve les 5 derniers messages."""
        self.message_log.append(message)
        if len(self.message_log) > 5:
            self.message_log.pop(0)

    def display_message_log(self):
        """Affiche les messages du log dans une zone dédiée."""
        start_y = 100  # Position verticale de départ
        for i, message in enumerate(self.message_log):
            draw_text(self.screen, message, 500, start_y + i * 30)

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

            player_x, player_y = 100 + oscillation , 350 - oscillation
            opponent_x, opponent_y = 550 - oscillation , 200 + oscillation


            # Dessiner les Pokémon avec leurs effets visuels
            self.player_pokemon.draw(self.screen, player_x, player_y)
            self.opponent_pokemon.draw(self.screen, opponent_x, opponent_y)

            # Affiche le log de messages à l'écran
            self.display_message_log()

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
                self.add_message(f"{winner.capitalize()} wins!")
                self.display_message_log()
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

            self.add_message(f"{self.player_pokemon.name.capitalize()} used {attack.name}!")
            if critical:
                self.add_message("🔥 Critical hit!")
            if effectiveness > 1:
                self.add_message("It's super effective!")
            elif effectiveness < 1:
                self.add_message("It's not very effective...")
            self.add_message(f"{self.player_pokemon.name.capitalize()} dealt {damage} damage!")
        else:
            self.add_message(f"{attack.name} n'a plus de PP!")

    def opponent_attack(self):
        """ L'IA choisit une attaque aléatoire et affiche le feedback sur la fenêtre """
        move = random.choice(self.player_moves)
        damage, effectiveness, critical, _ = self.combat.apply_damage(self.opponent_pokemon, self.player_pokemon, move)

        self.add_message(f"{self.opponent_pokemon.name.capitalize()} used {move.name}!")
        if critical:
            self.add_message("🔥 Critical hit!")
        if effectiveness > 1:
            self.add_message("It's super effective!")
        elif effectiveness < 1:
            self.add_message("It's not very effective...")
        self.add_message(f"{self.opponent_pokemon.name.capitalize()} dealt {damage} damage!")