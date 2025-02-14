import json
import os
import requests
from pokemon import Pokemon

# Définition du fichier JSON pour stocker les données
TYPE_CHART_PATH = "type_chart.json"

# Fonction pour récupérer les relations de types depuis l'API
def fetch_type_chart():
    type_chart = {}

    for type_name in ["normal", "fire", "water", "electric", "grass", "ice", "fighting", "poison", "ground",
                      "flying", "psychic", "bug", "rock", "ghost", "dragon", "dark", "steel", "fairy"]:
        url = f"https://pokeapi.co/api/v2/type/{type_name}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            damage_relations = data["damage_relations"]
            
            type_chart[type_name] = {
                "double_damage_to": [t["name"] for t in damage_relations["double_damage_to"]],
                "half_damage_to": [t["name"] for t in damage_relations["half_damage_to"]],
                "no_damage_to": [t["name"] for t in damage_relations["no_damage_to"]]
            }

    # Sauvegarde en cache pour éviter de faire trop d'appels API
    with open(TYPE_CHART_PATH, "w") as file:
        json.dump(type_chart, file, indent=4)

    return type_chart

# Charger ou récupérer le tableau des types
if os.path.exists(TYPE_CHART_PATH):
    with open(TYPE_CHART_PATH, "r") as file:
        type_chart = json.load(file)
else:
    type_chart = fetch_type_chart()


class Combat:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    def damage_effectiveness(self, attacker, defender):
        attacker_type = attacker.types[0] if attacker.types else "normal"
        defender_type = defender.types[0] if defender.types else "normal"

        # Vérification des types existants
        if attacker_type not in type_chart or defender_type not in type_chart:
            return 1  # Retourne un multiplicateur neutre si le type est inconnu

        # Calcul de l'efficacité
        if defender_type in type_chart[attacker_type]["double_damage_to"]:
            return 2  # Super efficace
        elif defender_type in type_chart[attacker_type]["half_damage_to"]:
            return 0.5  # Pas très efficace
        elif defender_type in type_chart[attacker_type]["no_damage_to"]:
            return 0  # Aucun effet
        else:
            return 1  # Neutre

    def apply_damage(self, attacker, defender):
        effectiveness = self.damage_effectiveness(attacker, defender)
        damage = (attacker.stats.get("attack", 10) * effectiveness) - defender.stats.get("defense", 5)
        damage = max(1, damage)  # S'assurer que le dégât est au minimum de 1 PV

        defender.stats["hp"] -= damage
        return damage

    def winner(self):
        if self.enemy.stats["hp"] <= 0:
            return self.player.name, self.enemy.name
        elif self.player.stats["hp"] <= 0:
            return self.enemy.name, self.player.name
        else:
            return None, None