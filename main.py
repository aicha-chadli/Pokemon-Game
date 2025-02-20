import pygame
from src.menu import MainMenu

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pokémon Game")

    main_menu = MainMenu(screen)
    main_menu.run()

if __name__ == "__main__":
    main()