import pygame
import os

class SoundManager:
    def __init__(self):
        # Asegurarse de que pygame.mixer esté inicializado correctamente
        try:
            pygame.mixer.init(44100, -16, 2, 2048)
        except pygame.error:
            print("No se pudo inicializar el sistema de audio")
        
        self.current_music = None
        
        # Definir la ruta base para los archivos de música
        self.sound_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sounds")
        
        # Rutas de los archivos de música
        self.music_files = {
            'menu': os.path.join(self.sound_dir, 'menu.mp3'),
            'pokedex': os.path.join(self.sound_dir, 'pokedex.mp3'),
            'combat': os.path.join(self.sound_dir, 'combat.mp3')
        }
        
    def play_music(self, music_type):
        """
        Reproduce la música especificada en loop
        music_type puede ser: 'menu', 'pokedex', 'combat'
        """
        if self.current_music != music_type:
            try:
                pygame.mixer.music.stop()
                music_file = self.music_files.get(music_type)
                
                if music_file and os.path.exists(music_file):
                    pygame.mixer.music.load(music_file)
                    pygame.mixer.music.play(-1)  # -1 significa loop infinito
                    self.current_music = music_type
                else:
                    print(f"Archivo de música no encontrado: {music_file}")
                    
            except pygame.error as e:
                print(f"Error al reproducir la música: {e}")
                # Intentar cargar un formato alternativo
                try:
                    alt_file = music_file.replace('.mp3', '.wav')
                    if os.path.exists(alt_file):
                        pygame.mixer.music.load(alt_file)
                        pygame.mixer.music.play(-1)
                        self.current_music = music_type
                except:
                    print("No se pudo cargar el formato alternativo")
