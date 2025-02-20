from pydub import AudioSegment

def convert_to_wav():
    for music_type in ['menu', 'pokedex', 'combat']:
        mp3_path = f'assets/sounds/{music_type}.mp3'
        wav_path = f'assets/sounds/{music_type}.wav'
        
        if os.path.exists(mp3_path):
            sound = AudioSegment.from_mp3(mp3_path)
            sound.export(wav_path, format='wav')

convert_to_wav()