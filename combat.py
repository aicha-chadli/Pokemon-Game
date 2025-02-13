import json
import os
from pokemon import Pokemon

# Check if the files exist before trying to open them
pokemon_json_path = os.path.abspath("data\pokemon.json")
pokedex_json_path = os.path.abspath("data\pokedex.json")

if not os.path.exists(pokemon_json_path):
    raise FileNotFoundError(f"No such file or directory: '{pokemon_json_path}'")
if not os.path.exists(pokedex_json_path):
    raise FileNotFoundError(f"No such file or directory: '{pokedex_json_path}'")

with open(pokemon_json_path, "r") as file:
    pokemon_json = json.load(file)

# Handle the case where pokedex.json is empty or does not contain valid JSON
try:
    with open(pokedex_json_path, "r") as file:
        pokedex_json = json.load(file)
except json.JSONDecodeError:
    pokedex_json = {}

class Combat():
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    def damage_effectiveness(self, attacker, defender):
        attacker_type = attacker.types[0]
        defender_type = defender.types[0]
        type_effectiveness = {
            "normal": {"Normal": 1, "fire": 1, "water": 1, "electric": 1, "grass": 1, "ice": 1, "fighting": 1, "poison": 1, "ground": 1, "flying": 1, "psychic": 1, "bug": 1, "rock": 0.5, "ghost": 0, "dragon": 1, "dark": 1, "steel": 0.5, "fairy": 1},
            "steel": {"Normal": 1, "fire": 0.5, "water": 0.5, "electric": 1, "grass": 2, "ice": 2, "fighting": 1, "poison": 1, "ground": 1, "flying": 1, "psychic": 1, "bug": 2, "rock": 0.5, "ghost": 1, "dragon": 0.5, "dark": 1, "steel": 2, "fairy": 1},
            "water": {"Normal": 1, "fire": 2, "water": 0.5, "electric": 1, "grass": 0.5, "ice": 1, "fighting": 1, "poison": 1, "ground": 2, "flying": 1, "psychic": 1, "bug": 1, "rock": 2, "ghost": 1, "dragon": 0.5, "dark": 1, "steel": 1, "fairy": 1},
            "electric": {"Normal": 1, "fire": 1, "water": 2, "electric": 0.5, "grass": 0.5, "ice": 1, "fighting": 1, "poison": 1, "ground": 0, "flying": 2, "psychic": 1, "bug": 1, "rock": 1, "ghost": 1, "dragon": 0.5, "dark": 1, "steel": 1, "fairy": 1},
            "grass": {"Normal": 1, "fire": 0.5, "water": 2, "electric": 1, "grass": 0.5, "ice": 1, "fighting": 1, "poison": 0.5, "ground": 2, "flying": 0.5, "psychic": 1, "bug": 0.5, "rock": 2, "ghost": 1, "dragon": 0.5, "dark": 1, "steel": 0.5, "fairy": 1},
            "ice": {"Normal": 1, "fire": 0.5, "water": 0.5, "electric": 1, "grass": 2, "ice": 0.5, "fighting": 1, "poison": 1, "ground": 2, "flying": 2, "psychic": 1, "bug": 1, "rock": 1, "ghost": 1, "dragon": 2, "dark": 1, "steel": 0.5, "fairy": 1},
            "fighting": {"Normal": 2, "fire": 1, "water": 1, "electric": 1, "grass": 1, "ice": 2, "fighting": 1, "poison": 0.5, "ground": 1, "flying": 0.5, "psychic": 0.5, "bug": 0.5, "rock": 2, "ghost": 0, "dragon": 1, "dark": 2, "steel": 2, "fairy": 0.5},
            "poison": {"Normal": 1, "fire": 1, "water": 1, "electric": 1, "grass": 2, "ice": 1, "fighting": 1, "poison": 0.5, "ground": 0.5, "flying": 1, "psychic": 1, "bug": 1, "rock": 0.5, "ghost": 0.5, "dragon": 1, "dark": 1, "steel": 0, "fairy": 2},
            "ground": {"Normal": 1, "fire": 2, "water": 1, "electric": 2, "grass": 0.5, "ice": 1, "fighting": 1, "poison": 2, "ground": 1, "flying": 0, "psychic": 1, "bug": 0.5, "rock": 2, "ghost": 1, "dragon": 1, "dark": 1, "steel": 2, "fairy": 1},
            "flying": {"Normal": 1, "fire": 1, "water": 1, "electric": 0.5, "grass": 2, "ice": 1, "fighting": 2, "poison": 1, "ground": 1, "flying": 1, "psychic": 1, "bug": 2, "rock": 0.5, "ghost": 1, "dragon": 1, "dark": 1, "steel": 0.5, "fairy": 1},
            "psychic": {"Normal": 1, "fire": 1, "water": 1, "electric": 1, "grass": 1, "ice": 1, "fighting": 2, "poison": 2, "ground": 1, "flying": 1, "psychic": 0.5, "bug": 1, "rock": 1, "ghost": 1, "dragon": 1, "dark": 0, "steel": 0.5, "fairy": 1},
            "bug": {"Normal": 1, "fire": 0.5, "water": 1, "electric": 1, "grass": 2, "ice": 1, "fighting": 0.5, "poison": 0.5, "ground": 1, "flying": 0.5, "psychic": 2, "bug": 1, "rock": 1, "ghost": 0.5, "dragon": 1, "dark": 2, "steel": 0.5, "fairy": 0.5},
            "rock": {"Normal": 1, "fire": 2, "water": 1, "electric": 1, "grass": 1, "ice": 2, "fighting": 0.5, "poison": 1, "ground": 0.5, "flying": 2, "psychic": 1, "bug": 2, "rock": 1, "ghost": 1, "dragon": 1, "dark": 1, "steel": 0.5, "fairy": 1},
            "ghost": {"Normal": 0, "fire": 1, "water": 1, "electric": 1, "grass": 1, "ice": 1, "fighting": 1, "poison": 1, "ground": 1, "flying": 1, "psychic": 2, "bug": 1, "rock": 1, "ghost": 2, "dragon": 1, "dark": 0.5, "steel": 1, "fairy": 1},
            "dragon": {"Normal": 1, "fire": 1, "water": 1, "electric": 1, "grass": 1, "ice": 1, "fighting": 1, "poison": 1, "ground": 1, "flying": 1, "psychic": 1, "bug": 1, "rock": 1, "ghost": 1, "dragon": 2, "dark": 1, "steel": 0.5, "fairy": 0},
            "dark": {"Normal": 1, "fire": 1, "water": 1, "electric": 1, "grass": 1, "ice": 1, "fighting": 0.5, "poison": 1, "ground": 1, "flying": 1, "psychic": 2, "bug": 1, "rock": 1, "ghost": 2, "dragon": 1, "dark": 0.5, "steel": 1, "fairy": 0.5},
            "steel": {"Normal": 1, "fire": 0.5, "water": 0.5, "electric": 0.5, "grass": 1, "ice": 2, "fighting": 1, "poison": 1, "ground": 1, "flying": 1, "psychic": 1, "bug": 1, "rock": 2, "ghost": 1, "dragon": 1, "dark": 1, "steel": 0.5, "fairy": 2},
            "fairy": {"Normal": 1, "fire": 0.5, "water": 1, "electric": 1, "grass": 1, "ice": 1, "fighting": 2, "poison": 0.5, "ground": 1, "flying": 1, "psychic": 1, "bug": 1, "rock": 1, "ghost": 1, "dragon": 2, "dark": 2, "steel": 0.5, "fairy": 1}
        }
        return type_effectiveness[attacker_type].get(defender_type, 1)

    def apply_damage(self, attacker, defender):
        damage_multiplied = attacker.attack_power * self.damage_effectiveness(attacker, defender)
        damage = damage_multiplied - defender.defense
        defender.life_points -= damage
        return defender.life_points

    def winner(self):
        if self.enemy.life_points <= 0:
            winner=self.player.name
            loser=self.enemy.name
            return winner, loser
        elif self.player.life_points <= 0:
            winner=self.enemy.name
            loser=self.player.name
            return winner, loser
        else:
            return None, None
    
    def send_to_pokedex(self, loser, winner):
        with open(pokedex_json_path, "r") as file:
            pokedex = json.load(file)
        
        if loser == self.enemy.name:
            pokedex[self.enemy.name] = {
                "types": self.enemy.types,
                "attack_power": self.enemy.attack_power,
                "defense": self.enemy.defense,
                "life_points": self.enemy.life_points
            }
        
        if winner == self.player.name:
            pokedex[self.player.name] = {
                "types": self.player.types,
                "attack_power": self.player.attack_power,
                "defense": self.player.defense,
                "life_points": self.player.life_points
            }
        
        with open(pokedex_json_path, "w") as file:
            json.dump(pokedex, file, indent=4)


#############

# Creating Pokemon instances
player = Pokemon(name="Pikachu", types=["electric","ghost"], attack_power=55, defense=40, life_points=100, level=1, x=0, y=0)
enemy = Pokemon(name="Charmander", types=["fire"], attack_power=52, defense=43, life_points=100, level=1, x=0, y=0)

# Create a Combat instance
combat = Combat(player, enemy)

# Apply damage and determine the winner
print(enemy.life_points)
combat.apply_damage(player, enemy)
combat.apply_damage(player, enemy)
print(enemy.life_points)
combat.apply_damage(player, enemy)
combat.apply_damage(player, enemy)
print(enemy.life_points)
combat.apply_damage(player, enemy)
combat.apply_damage(player, enemy)
print(enemy.life_points)
combat.apply_damage(player, enemy)
combat.apply_damage(player, enemy)
print(enemy.life_points)
combat.apply_damage(player, enemy)
print(enemy.life_points)
winner, loser = combat.winner()
print(f"Winner: {winner}, Loser: {loser}")

# Send to the Pokedex the loser if it is the enemy 
# and the player's Pokemon if he/she has won
combat.send_to_pokedex(loser, winner)