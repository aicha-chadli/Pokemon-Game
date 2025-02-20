import os
from pydub import AudioSegment

def convert_to_wav():
    for music_type in ['menu', 'pokedex', 'combat']:
        mp3_path = f'assets/sounds/{music_type}.mp3'
        wav_path = f'assets/sounds/{music_type}.wav'
        
        if os.path.exists(mp3_path):
            try:
                # Charger le fichier MP3
                sound = AudioSegment.from_mp3(mp3_path)
                
                # Exporter en WAV
                sound.export(wav_path, format='wav')
                print(f"Conversion réussie : {mp3_path} -> {wav_path}")
            except Exception as e:
                print(f"Erreur lors de la conversion de {mp3_path} : {e}")
        else:
            print(f"Fichier MP3 non trouvé : {mp3_path}")

convert_to_wav()
