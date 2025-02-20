import pygame
import random
import math

class Effect:
    def __init__(self, x, y, type_name):
        self.x = x
        self.y = y
        self.type_name = type_name
        self.lifetime = 30  # duración del efecto en frames
        self.particles = []
        self.initialize_particles()
    
    def initialize_particles(self):
        if self.type_name == "fire":
            # Partículas de fuego (rojas y naranjas)
            for _ in range(20):
                particle = {
                    'x': self.x,
                    'y': self.y,
                    'dx': random.uniform(-2, 2),
                    'dy': random.uniform(-4, -1),
                    'size': random.randint(3, 6),
                    'color': random.choice([(255,0,0), (255,69,0), (255,140,0)])
                }
                self.particles.append(particle)
        
        elif self.type_name == "water":
            # Gotas de agua (azules)
            for _ in range(15):
                particle = {
                    'x': self.x,
                    'y': self.y,
                    'dx': random.uniform(-1.5, 1.5),
                    'dy': random.uniform(-3, 3),
                    'size': random.randint(2, 5),
                    'color': random.choice([(0,0,255), (0,191,255), (30,144,255)])
                }
                self.particles.append(particle)
        
        elif self.type_name == "electric":
            # Rayos eléctricos (amarillos)
            for _ in range(10):
                particle = {
                    'x': self.x,
                    'y': self.y,
                    'dx': random.uniform(-3, 3),
                    'dy': random.uniform(-3, 3),
                    'size': random.randint(2, 4),
                    'color': (255,255,0)
                }
                self.particles.append(particle)
        
        elif self.type_name == "grass":
            # Hojas verdes
            for _ in range(15):
                particle = {
                    'x': self.x,
                    'y': self.y,
                    'dx': random.uniform(-2, 2),
                    'dy': random.uniform(-2, 2),
                    'size': random.randint(3, 6),
                    'color': random.choice([(34,139,34), (0,255,0), (50,205,50)])
                }
                self.particles.append(particle)
        
        elif self.type_name == "psychic":
            # Energía psíquica (rosa/púrpura)
            for _ in range(15):
                particle = {
                    'x': self.x,
                    'y': self.y,
                    'dx': random.uniform(-2, 2) * math.cos(random.uniform(0, 2*math.pi)),
                    'dy': random.uniform(-2, 2) * math.sin(random.uniform(0, 2*math.pi)),
                    'size': random.randint(3, 6),
                    'color': random.choice([(255,0,255), (238,130,238), (147,112,219)])
                }
                self.particles.append(particle)
        
        else:
            # Efecto genérico (blanco)
            for _ in range(12):
                particle = {
                    'x': self.x,
                    'y': self.y,
                    'dx': random.uniform(-2, 2),
                    'dy': random.uniform(-2, 2),
                    'size': random.randint(2, 5),
                    'color': (255,255,255)
                }
                self.particles.append(particle)

    def update(self):
        self.lifetime -= 1
        for particle in self.particles:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            
            # Efectos específicos según el tipo
            if self.type_name == "fire":
                particle['dy'] -= 0.1  # El fuego sube
                particle['size'] = max(0, particle['size'] - 0.1)  # Se hace más pequeño
            elif self.type_name == "electric":
                particle['dx'] = random.uniform(-3, 3)  # Movimiento errático
            elif self.type_name == "psychic":
                # Movimiento circular
                angle = math.atan2(particle['dy'], particle['dx'])
                angle += 0.1
                speed = math.sqrt(particle['dx']**2 + particle['dy']**2)
                particle['dx'] = speed * math.cos(angle)
                particle['dy'] = speed * math.sin(angle)

    def draw(self, screen):
        for particle in self.particles:
            pygame.draw.circle(screen, particle['color'], 
                             (int(particle['x']), int(particle['y'])), 
                             int(particle['size']))

    def is_finished(self):
        return self.lifetime <= 0