from pymongo import MongoClient
import csv

# Chemin vers le fichier CSV téléchargé
csv_file_path = 'D:/Cours_NoSQL/Exercice_01/pokemonGO.csv'  # Assurez-vous que le chemin est correct

# Connexion à MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['PokemonDB']

# Création de la collection 'Pokemons' dans la base de données 'PokemonDB'
collection = db['Pokemons']
print("Base de données et collection créées avec succès")

# Insertion des données Pokémon
with open(csv_file_path, 'r') as file:
    reader = csv.DictReader(file)
    pokemon_list = list(reader)
    collection.insert_many(pokemon_list)
    print("Données Pokémon insérées avec succès")

# Lecture des données Pokémon
# Trouver tous les Pokémon de type "Feu"
fire_pokemons = collection.find({ "type": "Feu" })
print("Pokémon de type 'Feu':")
for pokemon in fire_pokemons:
    print(pokemon)

# Récupérer les informations du Pokémon nommé "Pikachu"
pikachu = collection.find_one({ "name": "Pikachu" })
print("Informations sur Pikachu:")
print(pikachu)

# Mise à jour des points de combat (CP) de "Pikachu" pour qu'ils soient de 900
collection.update_one(
    { "name": "Pikachu" },
    { "$set": { "CP": 900 } }
)
print("Mise à jour des points de combat de Pikachu effectuée avec succès")

# Suppression du Pokémon "Bulbasaur"
collection.delete_one({ "name": "Bulbasaur" })
print("Suppression de Bulbasaur effectuée avec succès")
