import pygame
import json
import requests
from io import BytesIO
from poke_api import get_pokemon_info

# Initialisation de pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
font = pygame.font.Font(None, 36)

# Charger le Pokédex depuis un fichier JSON
def load_pokedex():
    try:
        with open("pokedex.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_pokedex(pokedex):
    with open("pokedex.json", "w") as file:
        json.dump(pokedex, file, indent=4)

pokedex = load_pokedex()

# Fonction pour ajouter un Pokémon au Pokédex
def add_pokemon_to_pokedex(pokemon_name):
    global pokedex
    pokemon_data = get_pokemon_info(pokemon_name)
    if pokemon_data and pokemon_name.lower() not in [p["name"].lower() for p in pokedex]:
        pokedex.append(pokemon_data)
        save_pokedex(pokedex)

# Fonction pour afficher un menu
def draw_text(text, x, y):
    label = font.render(text, True, (255, 255, 255))
    screen.blit(label, (x, y))

def launch_game():
    input_text = ""
    active = False
    selected_pokemon = None
    
    running_game = True
    while running_game:
        screen.fill((0, 0, 0))
        draw_text("Entrez le nom du Pokémon :", 200, 100)
        draw_text(input_text, 300, 150)
        draw_text("Appuyez sur Entrée pour valider", 200, 200)
        
        if selected_pokemon:
            draw_text(f"{selected_pokemon['name']}", 400, 300)
            y_offset = 350
            for stat, value in selected_pokemon["stats"].items():
                draw_text(f"{stat}: {value}", 400, y_offset)
                y_offset += 30
            response = requests.get(selected_pokemon["sprite"])
            pokemon_image = pygame.image.load(BytesIO(response.content))
            screen.blit(pokemon_image, (500, 250))
            draw_text("Appuyez sur C pour choisir ce Pokémon", 200, 550)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_game = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running_game = False
                elif event.key == pygame.K_RETURN:
                    selected_pokemon = get_pokemon_info(input_text)
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_c and selected_pokemon:
                    print(f"{selected_pokemon['name']} sélectionné pour le combat !")
                    running_game = False
                else:
                    input_text += event.unicode

running = True
while running:
    screen.fill((0, 0, 0))
    draw_text("1. Lancer une partie", 300, 200)
    draw_text("2. Ajouter un Pokémon", 300, 250)
    draw_text("3. Voir le Pokédex", 300, 300)
    draw_text("4. Quitter", 300, 350)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                launch_game()
            elif event.key == pygame.K_2:
                pokemon_name = input("Entrez le nom du Pokémon : ")
                add_pokemon_to_pokedex(pokemon_name)
            elif event.key == pygame.K_3:
                print("--- Pokédex ---")
                for p in pokedex:
                    print(f"{p['name']} - Attaque: {p['stats']['attack']}, Défense: {p['stats']['defense']}, PV: {p['stats']['hp']}")
            elif event.key == pygame.K_4:
                running = False

pygame.quit()