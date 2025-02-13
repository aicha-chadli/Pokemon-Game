import pygame

def draw_text(screen, text, x, y, font_size=36, color=(255, 255, 255)):
    font = pygame.font.Font(None, font_size)
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def draw_button(screen, text, x, y, width, height, color=(0, 0, 0), text_color=(255, 0, 0)):
    pygame.draw.rect(screen, color, (x, y, width, height))
    draw_text(screen, text, x + 10, y + 10, font_size=24, color=text_color)

def draw_bordered_rect(screen, x, y, width, height, fill_color, border_color, border_width=2):
    """
    Dessine un rectangle avec une bordure.
    :param screen: Surface Pygame où dessiner.
    :param x: Position x du rectangle.
    :param y: Position y du rectangle.
    :param width: Largeur du rectangle.
    :param height: Hauteur du rectangle.
    :param fill_color: Couleur de remplissage du rectangle.
    :param border_color: Couleur de la bordure.
    :param border_width: Épaisseur de la bordure.
    """
    # Dessiner la bordure
    pygame.draw.rect(screen, border_color, (x, y, width, height))
    # Dessiner le rectangle intérieur
    pygame.draw.rect(screen, fill_color, (x + border_width, y + border_width, width - 2 * border_width, height - 2 * border_width))