from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient('localhost', 27017)
db = client['testDB']
collection = db['testCollection']

def explore_databases_and_collections():
    """Partie 1: Exploration des Bases de Données et Collections"""
    # Lancer mongosh pour démarrer le shell MongoDB
    # Lister les Bases de Données
    databases = client.list_database_names()
    print("Bases de données existantes:")
    print(databases)

    # Sélectionner une Base de Données
    db = client['testDB']
    print("Base de données sélectionnée: testDB")

    # Créer une Collection
    collection = db['testCollection']
    db.create_collection("testCollection")
    print("Collection créée: testCollection")

    # Afficher les Collections
    collections = db.list_collection_names()
    print("Collections dans testDB:")
    print(collections)

def manipulate_data():
    """Partie 2: Manipulation des Données"""
    # Insertion de Données
    result = collection.insert_one({"name": "test", "value": 1})
    print("Document inséré avec id:", result.inserted_id)

    # Lecture de Données
    documents = collection.find()
    print("Documents dans testCollection:")
    for doc in documents:
        print(doc)

    # Mise à Jour de Données
    result = collection.update_one({"name": "test"}, {"$inc": {"value": 1}})
    print("Documents mis à jour:", result.modified_count)

    # Suppression de Données
    result = collection.delete_one({"name": "test"})
    print("Documents supprimés:", result.deleted_count)

def cleanup():
    """Partie 3: Nettoyage"""
    # Suppression de Collection
    collection.drop()
    print("Collection testCollection supprimée")

    # Suppression de Base de Données
    db.command("dropDatabase")
    print("Base de données testDB supprimée")

def validate():
    """Validation des opérations"""
    # Vérifier la création de la base de données et de la collection
    databases = client.list_database_names()
    print("Bases de données:")
    print(databases)
    if 'testDB' in databases:
        print("La base de données testDB existe.")
        collections = db.list_collection_names()
        print("Collections dans testDB:")
        print(collections)
        if 'testCollection' in collections:
            print("La collection testCollection existe.")

    # Vérifier l'insertion des données
    documents = collection.find()
    print("Documents dans testCollection:")
    for doc in documents:
        print(doc)

    # Vérifier les opérations de lecture, de mise à jour et de suppression
    manipulate_data()
    documents = collection.find()
    print("Documents après mise à jour:")
    for doc in documents:
        print(doc)
    collection.delete_one({"name": "test"})
    documents = collection.find()
    print("Documents après suppression:")
    for doc in documents:
        print(doc)

if __name__ == "__main__":
    explore_databases_and_collections()
    manipulate_data()
    cleanup()
    validate()
