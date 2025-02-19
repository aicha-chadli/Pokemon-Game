import pygame

def draw_text(screen, text, x, y, font_size=30, color=(255,255,255)):
    """
    Dibuja texto en la pantalla con el color especificado
    :param screen: superficie de pygame donde dibujar
    :param text: texto a dibujar
    :param x: posición x
    :param y: posición y
    :param font_size: tamaño de la fuente (default: 30)
    :param color: color del texto en formato RGB (default: blanco)
    """
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))