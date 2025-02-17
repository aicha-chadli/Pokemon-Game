import json
import os
from pokemon import Pokemon

# Définition du fichier pour stocker les relations de types
TYPE_CHART_PATH = "type_chart.json"

# Base de données des relations de types (extraites de PokéAPI)
type_chart = {
    "normal": {"double_damage_to": [], "half_damage_to": ["rock", "steel"], "no_damage_to": ["ghost"]},
    "fire": {"double_damage_to": ["grass", "ice", "bug", "steel"], "half_damage_to": ["fire", "water", "rock", "dragon"], "no_damage_to": []},
    "water": {"double_damage_to": ["fire", "ground", "rock"], "half_damage_to": ["water", "grass", "dragon"], "no_damage_to": []},
    "electric": {"double_damage_to": ["water", "flying"], "half_damage_to": ["electric", "grass", "dragon"], "no_damage_to": ["ground"]},
    "grass": {"double_damage_to": ["water", "ground", "rock"], "half_damage_to": ["fire", "grass", "poison", "flying", "bug", "dragon", "steel"], "no_damage_to": []},
    "ice": {"double_damage_to": ["grass", "ground", "flying", "dragon"], "half_damage_to": ["fire", "water", "ice", "steel"], "no_damage_to": []},
    "fighting": {"double_damage_to": ["normal", "ice", "rock", "dark", "steel"], "half_damage_to": ["poison", "flying", "psychic", "bug", "fairy"], "no_damage_to": ["ghost"]},
    "poison": {"double_damage_to": ["grass", "fairy"], "half_damage_to": ["poison", "ground", "rock", "ghost"], "no_damage_to": ["steel"]},
    "ground": {"double_damage_to": ["fire", "electric", "poison", "rock", "steel"], "half_damage_to": ["grass", "bug"], "no_damage_to": ["flying"]},
    "flying": {"double_damage_to": ["grass", "fighting", "bug"], "half_damage_to": ["electric", "rock", "steel"], "no_damage_to": []},
    "psychic": {"double_damage_to": ["fighting", "poison"], "half_damage_to": ["psychic", "steel"], "no_damage_to": ["dark"]},
    "bug": {"double_damage_to": ["grass", "psychic", "dark"], "half_damage_to": ["fire", "fighting", "poison", "flying", "ghost", "steel", "fairy"], "no_damage_to": []},
    "rock": {"double_damage_to": ["fire", "ice", "flying", "bug"], "half_damage_to": ["fighting", "ground", "steel"], "no_damage_to": []},
    "ghost": {"double_damage_to": ["psychic", "ghost"], "half_damage_to": ["dark"], "no_damage_to": ["normal"]},
    "dragon": {"double_damage_to": ["dragon"], "half_damage_to": ["steel"], "no_damage_to": ["fairy"]},
    "dark": {"double_damage_to": ["psychic", "ghost"], "half_damage_to": ["fighting", "dark", "fairy"], "no_damage_to": []},
    "steel": {"double_damage_to": ["ice", "rock", "fairy"], "half_damage_to": ["fire", "water", "electric", "steel"], "no_damage_to": []},
    "fairy": {"double_damage_to": ["fighting", "dragon", "dark"], "half_damage_to": ["fire", "poison", "steel"], "no_damage_to": []}
}

# Sauvegarde dans un fichier JSON local
if not os.path.exists(TYPE_CHART_PATH):
    with open(TYPE_CHART_PATH, "w") as file:
        json.dump(type_chart, file, indent=4)

class Combat:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    def damage_effectiveness(self, attacker, defender):
        attacker_type = attacker.types[0] if attacker.types else "normal"
        defender_type = defender.types[0] if defender.types else "normal"

        if attacker_type not in type_chart or defender_type not in type_chart:
            return 1  # Neutre si type inconnu

        if defender_type in type_chart[attacker_type]["double_damage_to"]:
            return 2  # Super efficace
        elif defender_type in type_chart[attacker_type]["half_damage_to"]:
            return 0.5  # Pas très efficace
        elif defender_type in type_chart[attacker_type]["no_damage_to"]:
            return 0  # Aucun effet
        else:
            return 1  # Normal

    def apply_damage(self, attacker, defender):
        effectiveness = self.damage_effectiveness(attacker, defender)
        damage = (attacker.stats["attack"] * effectiveness) - defender.stats["defense"]
        damage = max(1, damage)  # Min 1 PV

        defender.stats["hp"] -= damage
        return damage

    def winner(self):
        if self.enemy.stats["hp"] <= 0:
            return self.player.name, self.enemy.name
        elif self.player.stats["hp"] <= 0:
            return self.enemy.name, self.player.name
        else:
            return None, None