import pygame

class Pokemon:
    def __init__(self, name, life_points, level, attack_power, defense, evolution, type, x, y):
        # Character attributes
        self.name = name
        self.life_points = life_points
        self.level = level  # 
        self.attack_power = attack_power
        self.defense = defense 
        self.evolution = evolution    # "baby", "teen", "adult"
        self.type = type    # water, fire, grass & normal
        # GUI attributes
        self.image = pygame.image.load("player.png")
        self.image
        self.rect = self.image.get_rect(x=x, y=y)
        self.speed = 5
        self.velocity = [0, 0]  # x, y, x horizontal & vertical control.
                                # 0 is no movement. 
                                # Accelere if positive, decelere if negative.

    def draw(self, screen):
        screen.blit(self.image, self.rect)  # affiche l'image du joueur sur l'ecran a la position du rectangle