import requests

# Fonction pour récupérer les informations du Pokémon
def get_pokemon_info(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        # Extraire les stats et l'image du Pokémon
        stats = {stat["stat"]["name"]: stat["base_stat"] for stat in data["stats"]}
        sprite_url = data["sprites"]["front_default"]
        return {"name": name.capitalize(), "stats": stats, "sprite": sprite_url}
    else:
        print(f"Pokémon '{name}' non trouvé !")
        return None
