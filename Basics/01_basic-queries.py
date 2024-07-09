from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient('localhost', 27017)
db = client['PokemonDB']
collection = db['Pokemons']

def create_database_and_collection():
    """Exercice 1: Création d'une Base de Données et d'une Collection"""
    db = client['PokemonDB']
    collection = db['Pokemons']
    print("Base de données et collection créées.")

def insert_data():
    """Exercice 2: Insertion de Données"""
    # L'insertion des données se fait avec la commande mongoimport ci-dessus.
    pass

def read_data():
    """Exercice 3: Lecture de Données"""
    # Trouver tous les Pokémon de type "Feu"
    fire_pokemons = collection.find({"type": "Feu"})
    print("Pokémon de type 'Feu':")
    for pokemon in fire_pokemons:
        print(pokemon)

    # Récupérer les informations du Pokémon nommé "Pikachu"
    pikachu = collection.find_one({"name": "Pikachu"})
    print("Informations de Pikachu:")
    print(pikachu)

def update_data():
    """Exercice 4: Mise à Jour de Données"""
    # Mettre à jour les points de combat (CP) de "Pikachu" pour qu'ils soient de 900
    collection.update_one({"name": "Pikachu"}, {"$set": {"CP": 900}})
    print("Mise à jour des points de combat de Pikachu effectuée.")

def delete_data():
    """Exercice 5: Suppression d'Éléments"""
    # Supprimer le Pokémon "Bulbasaur" de la collection Pokemons
    collection.delete_one({"name": "Bulbasaur"})
    print("Bulbasaur supprimé de la collection.")

def validate():
    """Validation des opérations"""
    # Vérifier la création de la base de données et de la collection
    databases = client.list_database_names()
    print("Bases de données:")
    print(databases)
    if 'PokemonDB' in databases:
        print("La base de données PokemonDB existe.")
        collections = db.list_collection_names()
        print("Collections dans PokemonDB:")
        print(collections)
        if 'Pokemons' in collections:
            print("La collection Pokemons existe.")

    # Vérifier l'insertion des données
    pokemons = collection.find()
    print("Tous les Pokémons:")
    for pokemon in pokemons:
        print(pokemon)

    # Vérifier les opérations de lecture, de mise à jour et de suppression
    print("Validation des opérations de lecture, mise à jour et suppression:")
    read_data()
    update_data()
    pikachu = collection.find_one({"name": "Pikachu"})
    print("Après mise à jour:")
    print(pikachu)
    bulbasaur = collection.find_one({"name": "Bulbasaur"})
    if not bulbasaur:
        print("Bulbasaur a été supprimé.")

if __name__ == "__main__":
    create_database_and_collection()
    insert_data()  # Vous pouvez commenter cette ligne après l'importation initiale des données
    read_data()
    update_data()
    delete_data()
    validate()
