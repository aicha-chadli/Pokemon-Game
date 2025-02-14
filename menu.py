import pygame
from pokemon import Pokemon
from utils import draw_text
from game import Game 

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.pokemon_names = Pokemon.get_pokemon_names()  # Récupération des noms de Pokémon
        self.current_index = 0
        self.background_main_menu = pygame.image.load('background_pokemon.jpg')
        self.background_main_menu = pygame.transform.scale(self.background_main_menu, (800, 600))
        self.selected_pokemon = Pokemon(self.pokemon_names[self.current_index])  # Initialisation du premier Pokémon
        self.attack_effect = None  # Initialisation de l'effet visuel de l'attaque
        self.defense_effect = None  # Initialisation de l'effet visuel de la défense

    def run(self):
        running = True
        while running:
            self.screen.blit(self.background_main_menu, (0, 0))
            draw_text(self.screen, "1. Jouer", 280, 550)
            draw_text(self.screen, "2. Quitter", 450, 550)

            # Afficher l'effet visuel de l'attaque ou de la défense si activé
            if self.attack_effect:
                self.attack_effect.draw(self.screen, 350, 250)  # L'attaque du Pokémon sélectionné
            if self.defense_effect:
                self.defense_effect.draw(self.screen, 350, 250)  # La défense du Pokémon sélectionné
            
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.launch_game()
                    elif event.key == pygame.K_2:
                        running = False
                    elif event.key == pygame.K_LEFT:
                        self.current_index = (self.current_index - 1) % len(self.pokemon_names)
                    elif event.key == pygame.K_RIGHT:
                        self.current_index = (self.current_index + 1) % len(self.pokemon_names)
                    
                    # Mise à jour du Pokémon sélectionné et ajout des effets visuels
                    self.selected_pokemon = Pokemon(self.pokemon_names[self.current_index])
                    self.attack_effect = None
                    self.defense_effect = None

    def launch_game(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))  
            draw_text(self.screen, "← / → pour choisir un Pokémon", 200, 100)
            draw_text(self.screen, "C pour valider", 200, 150)
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
                    if event.key == pygame.K_LEFT:
                        self.current_index = (self.current_index - 1) % len(self.pokemon_names)
                    elif event.key == pygame.K_RIGHT:
                        self.current_index = (self.current_index + 1) % len(self.pokemon_names)
                    elif event.key == pygame.K_c:
                        # Lancer le combat avec le Pokémon sélectionné
                        game = Game(self.screen, self.selected_pokemon)
                        game.run()
                        running = False
                    
                    # Mise à jour du Pokémon sélectionné et réinitialisation des effets visuels
                    self.selected_pokemon = Pokemon(self.pokemon_names[self.current_index])
                    self.attack_effect = None
                    self.defense_effect = None
