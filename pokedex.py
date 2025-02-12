import json
from pokemon import Pokemon

class Pokedex:
    def __init__(self):
        self.pokedex = self._load_pokedex()

    def _load_pokedex(self):
        try:
            with open("pokedex.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_pokedex(self):
        with open("pokedex.json", "w") as file:
            json.dump(self.pokedex, file, indent=4)

    def add_pokemon(self, pokemon_name):
        pokemon = Pokemon(pokemon_name)
        if pokemon.image and pokemon_name.lower() not in [p["name"].lower() for p in self.pokedex]:
            self.pokedex.append({
                "name": pokemon.name,
                "types": pokemon.types,
                "stats": pokemon.stats,
                "sprite": f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_name.lower()}.png"
            })
            self.save_pokedex()
        else:
            print("❌ Pokémon introuvable ou déjà dans le Pokédex !")