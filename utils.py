import pygame

def draw_text(screen, text, x, y, font_size=30, color=(255, 255, 255)):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_bordered_rect(screen, x, y, width, height, color, border_color, border_width=2):
    pygame.draw.rect(screen, border_color, (x - border_width, y - border_width, width + 2 * border_width, height + 2 * border_width))
    pygame.draw.rect(screen, color, (x, y, width, height))