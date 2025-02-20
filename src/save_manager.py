import json
import os

class SaveManager:
    SAVE_FILE = "data/last_battle.json"

    @staticmethod
    def save_battle(player_pokemon, opponent_pokemon):
        """Guarda el último combate"""
        battle_data = {
            "player_pokemon": player_pokemon.name,
            "opponent_pokemon": opponent_pokemon.name
        }
        
        with open(SaveManager.SAVE_FILE, "w") as f:
            json.dump(battle_data, f)

    @staticmethod
    def load_last_battle():
        """Carga el último combate guardado"""
        if not os.path.exists(SaveManager.SAVE_FILE):
            return None, None
            
        try:
            with open(SaveManager.SAVE_FILE, "r") as f:
                battle_data = json.load(f)
                return battle_data["player_pokemon"], battle_data["opponent_pokemon"]
        except:
            return None, None