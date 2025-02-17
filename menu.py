import pygame
import math
from pokemon import Pokemon
from utils import draw_text
from game import Game

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.pokemon_names = Pokemon.get_pokemon_names()
        self.current_index = 0
        self.background_main_menu = pygame.image.load('background_pokemon.jpg')
        self.background_main_menu = pygame.transform.scale(self.background_main_menu, (800, 600))
        self.selected_pokemon = Pokemon(self.pokemon_names[self.current_index])
        self.attack_effect = None
        self.defense_effect = None

        # Chargement des boutons
        self.button_play_image = pygame.image.load('button_play.png')
        self.button_load_image = pygame.image.load('button_load.png')
        self.button_quit_image = pygame.image.load('button_quit.png')
        self.button_pokeball_image = pygame.image.load('pokeball.png')
        

        # Taille originale des boutons
        self.original_size = (70, 70)
        self.button_play_image = pygame.transform.scale(self.button_play_image, self.original_size)
        self.button_load_image = pygame.transform.scale(self.button_load_image, self.original_size)
        self.button_quit_image = pygame.transform.scale(self.button_quit_image, self.original_size)
        self.button_pokeball_image = pygame.transform.scale(self.button_pokeball_image, self.original_size)

        # Positions des boutons
        self.button_play_rect = self.button_play_image.get_rect(topleft=(230, 520))
        self.button_load_rect = self.button_load_image.get_rect(topleft=(370, 520))
        self.button_quit_rect = self.button_quit_image.get_rect(topleft=(500, 520))
        self.button_pokeball_rect = self.button_pokeball_image.get_rect(topleft=(20, 20))

        # Variables pour l'effet pulse
        self.pulse_speed = 0.1  # Vitesse du pulsation
        self.pulse_amplitude = 0.05  # Amplitude du pulsation
        self.frame = 0  # Compteur d'animation

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            self.screen.blit(self.background_main_menu, (0, 0))

            # Calcul du facteur de mise à l'échelle pour l'effet pulse
            scale_factor = 1 + math.sin(self.frame * self.pulse_speed) * self.pulse_amplitude

            # Appliquer l'effet pulse sur chaque bouton
            play_scaled = pygame.transform.scale(self.button_play_image, 
                                                 (int(self.original_size[0] * scale_factor), 
                                                  int(self.original_size[1] * scale_factor)))
            load_scaled = pygame.transform.scale(self.button_load_image, 
                                                 (int(self.original_size[0] * scale_factor), 
                                                  int(self.original_size[1] * scale_factor)))
            quit_scaled = pygame.transform.scale(self.button_quit_image, 
                                                 (int(self.original_size[0] * scale_factor), 
                                                  int(self.original_size[1] * scale_factor)))
            pokeball_scaled = pygame.transform.scale(self.button_pokeball_image, 
                                                 (int(self.original_size[0] * scale_factor), 
                                                  int(self.original_size[1] * scale_factor)))


            # Recalcule les nouvelles positions pour centrer les boutons après mise à l'échelle
            play_rect = play_scaled.get_rect(center=self.button_play_rect.center)
            load_rect = load_scaled.get_rect(center=self.button_load_rect.center)
            quit_rect = quit_scaled.get_rect(center=self.button_quit_rect.center)
            pokeball_rect = pokeball_scaled.get_rect(center=self.button_pokeball_rect.center)

            # Affichage des boutons avec effet pulse
            self.screen.blit(play_scaled, play_rect.topleft)
            self.screen.blit(load_scaled, load_rect.topleft)
            self.screen.blit(quit_scaled, quit_rect.topleft)
            self.screen.blit(pokeball_scaled, pokeball_rect.topleft)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.launch_game()
                    elif event.key == pygame.K_2 or event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_LEFT:
                        self.current_index = (self.current_index - 1) % len(self.pokemon_names)
                    elif event.key == pygame.K_RIGHT:
                        self.current_index = (self.current_index + 1) % len(self.pokemon_names)
                    self.selected_pokemon = Pokemon(self.pokemon_names[self.current_index])
                    self.attack_effect = None
                    self.defense_effect = None

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.button_play_rect.collidepoint(event.pos):
                            self.launch_game()
                        elif self.button_quit_rect.collidepoint(event.pos):
                            running = False

            self.frame += 1  # Incrémentation du compteur d'animation
            clock.tick(60)  # Limite à 60 FPS

    def launch_game(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))  
            draw_text(self.screen, "<-- / --> to choose a Pokémon", 200, 100)
            draw_text(self.screen, "C to validate", 200, 150)
            draw_text(self.screen, self.selected_pokemon.name.capitalize(), 350, 200)

            if self.selected_pokemon.image:
                self.screen.blit(self.selected_pokemon.image, (350, 250))

            y_offset = 400
            for stat, value in self.selected_pokemon.stats.items():
                draw_text(self.screen, f"{stat.capitalize()}: {value}", 350, y_offset)
                y_offset += 30

            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Retour au menu principal
                        return
                    elif event.key == pygame.K_LEFT:
                        self.current_index = (self.current_index - 1) % len(self.pokemon_names)
                    elif event.key == pygame.K_RIGHT:
                        self.current_index = (self.current_index + 1) % len(self.pokemon_names)
                    elif event.key == pygame.K_c:
                        game = Game(self.screen, self.selected_pokemon)
                        game.run()
                        running = False
                    
                    # Mise à jour du Pokémon sélectionné
                    self.selected_pokemon = Pokemon(self.pokemon_names[self.current_index])
                    self.attack_effect = None
                    self.defense_effect = None