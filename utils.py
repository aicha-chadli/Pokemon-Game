import pygame

def draw_text(screen, text, x, y, font_size=36, color=(255, 0, 0)):
    font = pygame.font.Font(None, font_size)
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def draw_button(screen, text, x, y, width, height, color=(0, 0, 0), text_color=(255, 255, 255)):
    pygame.draw.rect(screen, color, (x, y, width, height))
    draw_text(screen, text, x + 10, y + 10, font_size=24, color=text_color)