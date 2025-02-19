import json
import os
import requests
import random
from pokemon import Pokemon

TYPE_CHART_PATH = "type_chart.json"

# Fonction pour récupérer le tableau des types
def fetch_type_chart():
    type_chart = {}
    type_list = ["normal", "fire", "water", "electric", "grass", "ice", "fighting", "poison", "ground",
                 "flying", "psychic", "bug", "rock", "ghost", "dragon", "dark", "steel", "fairy"]

    for type_name in type_list:
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

    with open(TYPE_CHART_PATH, "w") as file:
        json.dump(type_chart, file, indent=4)

    return type_chart

if os.path.exists(TYPE_CHART_PATH):
    with open(TYPE_CHART_PATH, "r") as file:
        type_chart = json.load(file)
else:
    type_chart = fetch_type_chart()

# 🎯 Gestion des attaques
class Attack:
    def __init__(self, name, attack_type, power, pp, stat_modifier=None):
        self.name = name
        self.attack_type = attack_type
        self.power = power
        self.pp = pp  # Nombre de fois que l'attaque peut être utilisée
        self.stat_modifier = stat_modifier  # Peut modifier l'attaque ou la défense

    def use(self):
        if self.pp > 0:
            self.pp -= 1
            return True
        return False

# 📈 Gestion des changements de stats
class StatModifier:
    def __init__(self, target_stat, amount):
        self.target_stat = target_stat
        self.amount = amount  # Peut être positif (boost) ou négatif (malus)

    def apply(self, pokemon):
        pokemon.stats[self.target_stat] += self.amount
        return self.amount

# ⚔️ Classe Combat avec coups critiques et changements de stats
class Combat:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    def damage_effectiveness(self, attack_type, defender):
        defender_types = defender.types if defender.types else ["normal"]
        multiplier = 1

        for defender_type in defender_types:
            if attack_type in type_chart:
                if defender_type in type_chart[attack_type]["double_damage_to"]:
                    multiplier *= 2
                elif defender_type in type_chart[attack_type]["half_damage_to"]:
                    multiplier *= 0.5
                elif defender_type in type_chart[attack_type]["no_damage_to"]:
                    multiplier *= 0
        
        return multiplier

    def apply_damage(self, attacker, defender, attack):
        if attack.use():  # Vérifie si l'attaque a encore des PP
            effectiveness = self.damage_effectiveness(attack.attack_type, defender)

            level = attacker.level
            attack_stat = attacker.stats.get("attack", 10)
            defense_stat = defender.stats.get("defense", 5)
            power = attack.power

            # Formule de dégâts
            base_damage = (((2 * level / 5 + 2) * power * (attack_stat / defense_stat)) / 50) + 2
            base_damage *= effectiveness

            # Facteur aléatoire
            base_damage *= random.uniform(0.85, 1.0)

            # Coup critique (1/16 chance)
            critical = random.random() < 1/16
            if critical:
                base_damage *= 2

            damage = max(1, int(base_damage))
            defender.stats["hp"] -= damage

            # Mostrar el daño recibido
            defender.damage_text = str(damage)
            defender.damage_timer = 60  # Duración en frames (1 segundo a 60 FPS)

            # Appliquer un modificateur de stat si l'attaque en a un
            stat_change = None
            if attack.stat_modifier:
                stat_change = attack.stat_modifier.apply(defender)

            return damage, effectiveness, critical, stat_change
        return 0, 1, False, None  # Si pas de PP, pas de dégâts

    def winner(self):
        if self.enemy.stats["hp"] <= 0:
            return self.player.name, self.enemy.name
        elif self.player.stats["hp"] <= 0:
            return self.enemy.name, self.player.name
        return None, None
