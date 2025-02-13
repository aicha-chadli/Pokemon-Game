import pygame
from game import Game
from pokemon import Pokemon
from utils import draw_text, draw_bordered_rect

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.pokemon_names = Pokemon.get_pokemon_names()  # Appel à la méthode pour récupérer les noms
        self.current_index = 0
        self.background_main_menu = pygame.image.load('background_pokemon.jpg')  # Load background for main menu
        self.background_main_menu = pygame.transform.scale(self.background_main_menu, (800, 600))  # Resize background image

    def run(self):
        running = True
        while running:
            # Main menu background
            self.screen.blit(self.background_main_menu, (0, 0))  # Set the background
            draw_text(self.screen, "1. Play", 280, 550)
            draw_text(self.screen, "2. Quit", 450, 550)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.launch_game()
                    elif event.key == pygame.K_2:
                        running = False

    def launch_game(self):
        running = True
        selected_pokemon = Pokemon(self.pokemon_names[self.current_index])
        
        while running:
            self.screen.fill((0, 0, 0))  # Fond noir (black background for Pokémon selection)
            draw_text(self.screen, "Utilisez <- et -> pour choisir un Pokémon", 200, 100)
            draw_text(self.screen, "Appuyez sur C pour valider", 200, 150)
            
            draw_text(self.screen, selected_pokemon.name.capitalize(), 350, 200)
            
            if selected_pokemon.image:
                self.screen.blit(selected_pokemon.image, (350, 250))
            
            y_offset = 400
            for stat, value in selected_pokemon.stats.items():
                draw_text(self.screen, f"{stat.capitalize()}: {value}", 350, y_offset)
                y_offset += 30
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.current_index = (self.current_index - 1) % len(self.pokemon_names)
                        selected_pokemon = Pokemon(self.pokemon_names[self.current_index])
                    elif event.key == pygame.K_RIGHT:
                        self.current_index = (self.current_index + 1) % len(self.pokemon_names)
                        selected_pokemon = Pokemon(self.pokemon_names[self.current_index])
                    elif event.key == pygame.K_c:
                        game = Game(self.screen, selected_pokemon)
                        game.run()
                        running = False
