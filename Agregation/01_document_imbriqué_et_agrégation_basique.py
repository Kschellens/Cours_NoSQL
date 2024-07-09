import random
from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient('localhost', 27017)
db = client['PokemonDB']
collection = db['pokemonGO']

def add_random_stats():
    """Étape 1: Ajout de Statistiques Aléatoires"""
    pokemons = collection.find()
    for pokemon in pokemons:
        stats = {
            "attack": random.randint(1, 100),
            "defense": random.randint(1, 100)
        }
        collection.update_one({"_id": pokemon["_id"]}, {"$set": {"stats": stats}})
    print("Statistiques aléatoires ajoutées à chaque Pokémon.")

def aggregate_hp_cp():
    """Étape 2: Agrégation des Statistiques HP et CP"""
    # Moyenne des HP et des CP pour l'ensemble des Pokémon
    pipeline = [
        {"$group": {"_id": None, "averageHP": {"$avg": "$HP"}, "averageCP": {"$avg": "$CP"}}}
    ]
    result = collection.aggregate(pipeline)
    for doc in result:
        print("Moyenne des HP:", doc["averageHP"])
        print("Moyenne des CP:", doc["averageCP"])

    # Moyenne des HP et des CP par type
    pipeline = [
        {"$unwind": "$type"},
        {"$group": {"_id": "$type", "averageHP": {"$avg": "$HP"}, "averageCP": {"$avg": "$CP"}}}
    ]
    result = collection.aggregate(pipeline)
    for doc in result:
        print(f"Type: {doc['_id']}, Moyenne des HP: {doc['averageHP']}, Moyenne des CP: {doc['averageCP']}")

    # Pokémon ayant le HP et le CP les plus élevés
    max_hp = collection.find_one(sort=[("HP", -1)], projection={"_id": 0, "name": 1, "HP": 1})
    max_cp = collection.find_one(sort=[("CP", -1)], projection={"_id": 0, "name": 1, "CP": 1})
    print("Pokémon avec le plus de HP:", max_hp)
    print("Pokémon avec le plus de CP:", max_cp)

def read_specific_data():
    """Étape 3: Lecture de Données sur les Documents"""
    # Identifier tous les Pokémon avec plus de 50 d'attaques
    strong_pokemons = collection.find({"stats.attack": {"$gt": 50}})
    print("Pokémon avec plus de 50 d'attaques:")
    for pokemon in strong_pokemons:
        print(pokemon)

    # Sélectionner les Pokémon avec un CP supérieur à la moyenne des CP
    avg_cp = collection.aggregate([{"$group": {"_id": None, "averageCP": {"$avg": "$CP"}}}]).next()["averageCP"]
    high_cp_pokemons = collection.find({"CP": {"$gt": avg_cp}})
    print(f"Pokémon avec un CP supérieur à la moyenne ({avg_cp}):")
    for pokemon in high_cp_pokemons:
        print(pokemon)

def aggregate_by_type():
    """Étape 4: Agrégation des Statistiques par Type"""
    # Moyenne des statistiques d'attaque et de défense par type
    pipeline = [
        {"$unwind": "$type"},
        {"$group": {"_id": "$type", "averageAttack": {"$avg": "$stats.attack"}, "averageDefense": {"$avg": "$stats.defense"}}}
    ]
    result = collection.aggregate(pipeline)
    for doc in result:
        print(f"Type: {doc['_id']}, Moyenne des Attaques: {doc['averageAttack']}, Moyenne des Défenses: {doc['averageDefense']}")

def validate():
    """Validation des opérations"""
    pokemons = collection.find()
    print("Tous les Pokémon avec leurs statistiques:")
    for pokemon in pokemons:
        print(pokemon)

if __name__ == "__main__":
    add_random_stats()
    aggregate_hp_cp()
    read_specific_data()
    aggregate_by_type()
    validate()
