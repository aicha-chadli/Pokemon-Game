import json
import os
from pokemon import Pokemon

pokemon_json_path = "G:\LaPlateforme_\Periode 2\Python\Pokemon\Pokemon-Game\data\pokemon.json"
pokedex_json_path = ".G:\LaPlateforme_\Periode 2\Python\Pokemon\Pokemon-Game\data\pokedex.json"

# Verificar si los archivos existen antes de intentar abrirlos
if not os.path.exists(pokemon_json_path):
    raise FileNotFoundError(f"No such file or directory: '{pokemon_json_path}'")
if not os.path.exists(pokedex_json_path):
    raise FileNotFoundError(f"No such file or directory: '{pokedex_json_path}'")

with open(pokemon_json_path, "r") as file:
    pokemon_json = json.load(file)
with open(pokedex_json_path, "r") as file:
    pokedex_json = json.load(file)


class Combat():
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    def damage_multiplier(self, attacker, defender):
        type_effectiveness = {
            "water": {"water": 1, "fire": 2, "ground": 0.5, "electric": 0.5, "normal": 1},
            "fire": {"water": 0.5, "fire": 1, "ground": 2, "electric": 2, "normal": 1},
            "ground": {"water": 2, "fire": 0.5, "ground": 1, "electric": 2, "normal": 1},
            "electric": {"water": 0.5, "fire": 0.5, "ground": 1, "electric": 1, "normal": 1},
            "normal": {"water": 0.75, "fire": 0.75, "ground": 0.75, "electric": 0.75, "normal": 1}
        }
        return type_effectiveness[attacker.type].get(defender.type, 1)

    def apply_damage(self, attacker, defender):
        damage_multiplied = attacker.attack_power * self.damage_multiplier(attacker, defender)
        damage = damage_multiplied / defender.defense
        defender.life_points -= damage
        return defender.life_points

    def winner(self):
        if self.enemy.life_points <= 0:
            return self.player.name
        elif self.player.life_points <= 0:
            return self.enemy.name
        else:
            return "No one has won yet"
    
    def send_to_pokedex(self, loser):
        if loser == self.enemy.name:
            # Cargar el contenido actual del archivo pokedex.json
            with open(pokedex_json_path, "r") as file:
                pokedex = json.load(file)
            
            # Agregar el Pokémon enemigo al diccionario
            pokedex[self.enemy.name] = {
                "type": self.enemy.type,
                "attack_power": self.enemy.attack_power,
                "defense": self.enemy.defense,
                "life_points": self.enemy.life_points
            }
            
            # Guardar el diccionario actualizado en el archivo pokedex.json
            with open(pokedex_json_path, "w") as file:
                json.dump(pokedex, file, indent=4)

#############

# Crear instancias de Pokemon
player = Pokemon(name="Pikachu", type="electric", attack_power=55, defense=40, life_points=100)
enemy = Pokemon(name="Charmander", type="fire", attack_power=52, defense=43, life_points=100)

# Crear una instancia de Combat
combat = Combat(player, enemy)

# Aplicar daño y determinar el ganador
combat.apply_damage(player, enemy)
winner, loser = combat.winner()
print(f"Winner: {winner}, Loser: {loser}")

# Enviar al perdedor al Pokedex si es el enemigo
combat.send_to_pokedex(loser)