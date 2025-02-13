import pygame
from game import Game
from pokemon import Pokemon
from pokedex import Pokedex
from utils import draw_text, draw_button, draw_bordered_rect

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load("background_pokemon.jpg")  # Fond pour l'accueil
        self.background = pygame.transform.scale(self.background, (800, 600))
        self.pokedex = Pokedex()

    def run(self):
        running = True
        while running:
            self.screen.blit(self.background, (0, 0))  # Utiliser le fond d'accueil
            draw_text(self.screen, "1. Lancer une partie", 300, 200)
            draw_text(self.screen, "2. Ajouter un Pokémon", 300, 250)
            draw_text(self.screen, "3. Voir le Pokédex", 300, 300)
            draw_text(self.screen, "4. Quitter", 300, 350)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.launch_game()
                    elif event.key == pygame.K_2:
                        self.add_pokemon()
                    elif event.key == pygame.K_3:
                        self.view_pokedex()
                    elif event.key == pygame.K_4:
                        running = False

    def launch_game(self):
        input_text = ""
        selected_pokemon = None
        running = True

        while running:
            self.screen.blit(self.background, (0, 0))  # Fond d'accueil pendant la sélection
            draw_text(self.screen, "Entrez le nom du Pokémon :", 200, 100)
            draw_text(self.screen, input_text, 300, 150)
            draw_text(self.screen, "Appuyez sur Entrée pour valider", 200, 200)

            if selected_pokemon:
                # Cadre pour les caractéristiques du Pokémon
                draw_bordered_rect(self.screen, 390, 290, 350, 250, (255, 255, 255), (0, 0, 0))  # Bordure blanche avec contour noir
                draw_text(self.screen, f"{selected_pokemon.name.capitalize()}", 400, 300)
                draw_text(self.screen, f"Type(s) : {', '.join(selected_pokemon.types).capitalize()}", 400, 330)

                y_offset = 360
                for stat, value in selected_pokemon.stats.items():
                    draw_text(self.screen, f"{stat.capitalize()}: {value}", 400, y_offset)
                    y_offset += 30

                # Cadre pour l'image du Pokémon
                if selected_pokemon.image:
                    draw_bordered_rect(self.screen, 490, 240, 120, 120, (255, 255, 255), (0, 0, 0))  # Bordure blanche avec contour noir
                    self.screen.blit(selected_pokemon.image, (500, 250))  # Afficher l'image à droite

                draw_text(self.screen, "Appuyez sur C pour choisir ce Pokémon", 200, 550)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_RETURN:
                        # Valider le Pokémon entré
                        selected_pokemon = Pokemon(input_text)
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.key == pygame.K_c and selected_pokemon:
                        # Lancer le jeu avec le Pokémon choisi
                        game = Game(self.screen, selected_pokemon)
                        game.run()
                        running = False
                    else:
                        input_text += event.unicode

    def add_pokemon(self):
        pokemon_name = input("Entrez le nom du Pokémon : ")
        self.pokedex.add_pokemon(pokemon_name)

    def view_pokedex(self):
        print("--- Pokédex ---")
        for p in self.pokedex.pokedex:
            print(f"{p['name']} - Type(s): {', '.join(p['types'])} - PV: {p['stats']['hp']}")