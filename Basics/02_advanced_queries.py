from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient('localhost', 27017)
db = client['TitanicDB']
collection = db['Passengers']

def create_database_and_collection():
    """Exercice 1: Importation et Création de la Collection"""
    db = client['TitanicDB']
    collection = db['Passengers']
    print("Base de données et collection créées.")

def insert_data():
    """Exercice 2: Insertion de Données"""
    # L'insertion des données se fait avec la commande mongoimport ci-dessous.
    pass

def analyze_data():
    """Exercice 3: Analyse des Données"""
    # Compter le nombre total de passagers
    total_passengers = collection.count_documents({})
    print(f"Nombre total de passagers: {total_passengers}")

    # Trouver combien de passagers ont survécu
    survived_passengers = collection.count_documents({"Survived": 1})
    print(f"Nombre de passagers ayant survécu: {survived_passengers}")

    # Trouver le nombre de passagers femmes
    female_passengers = collection.count_documents({"Sex": "female"})
    print(f"Nombre de passagers femmes: {female_passengers}")

    # Trouver le nombre de passagers avec au moins 3 enfants
    passengers_with_children = collection.count_documents({"Parch": {"$gte": 3}})
    print(f"Nombre de passagers avec au moins 3 enfants: {passengers_with_children}")

def update_data():
    """Exercice 4: Mise à Jour de Données"""
    # Mettre à jour les documents pour lesquels le port d'embarquement est manquant
    collection.update_many({"Embarked": None}, {"$set": {"Embarked": "S"}})
    print("Port d'embarquement mis à jour pour les passagers manquants.")

    # Ajouter un champ `rescued` avec la valeur `true` pour tous les passagers qui ont survécu
    collection.update_many({"Survived": 1}, {"$set": {"rescued": True}})
    print("Champ 'rescued' ajouté pour les passagers ayant survécu.")

def complex_queries():
    """Exercice 5: Requêtes Complexes"""
    # Sélectionner les noms des 10 passagers les plus jeunes
    youngest_passengers = collection.find({}, {"Name": 1, "_id": 0}).sort("Age", 1).limit(10)
    print("Les 10 passagers les plus jeunes:")
    for passenger in youngest_passengers:
        print(passenger)

    # Identifier les passagers qui n'ont pas survécu et qui étaient dans la 2e classe
    non_survived_second_class = collection.find({"Survived": 0, "Pclass": 2}, {"Name": 1, "_id": 0})
    print("Passagers qui n'ont pas survécu et qui étaient dans la 2e classe:")
    for passenger in non_survived_second_class:
        print(passenger)

def delete_data():
    """Exercice 6: Suppression de Données"""
    # Supprimer les enregistrements des passagers qui n'ont pas survécu et dont l'âge est inconnu
    result = collection.delete_many({"Survived": 0, "Age": None})
    print(f"Enregistrements supprimés: {result.deleted_count}")

def bulk_update():
    """Exercice 7: Mise à Jour en Masse"""
    # Augmenter l'âge de tous les passagers de 1 an
    collection.update_many({}, {"$inc": {"Age": 1}})
    print("Âge de tous les passagers augmenté de 1 an.")

def conditional_delete():
    """Exercice 8: Suppression Conditionnelle"""
    # Supprimer les enregistrements des passagers qui n'ont pas de numéro de billet (Ticket)
    result = collection.delete_many({"Ticket": {"$exists": False}})
    print(f"Enregistrements supprimés: {result.deleted_count}")

def regex_query():
    """Bonus: Utiliser les REGEX"""
    # Utiliser une regex pour trouver tous les passagers qui porte le titre de `Dr.`
    doctors = collection.find({"Name": {"$regex": "Dr\."}}, {"Name": 1, "_id": 0})
    print("Passagers portant le titre de 'Dr.':")
    for doctor in doctors:
        print(doctor)

def validate():
    """Validation des opérations"""
    # Vérifier la création de la base de données et de la collection
    databases = client.list_database_names()
    print("Bases de données:")
    print(databases)
    if 'TitanicDB' in databases:
        print("La base de données TitanicDB existe.")
        collections = db.list_collection_names()
        print("Collections dans TitanicDB:")
        print(collections)
        if 'Passengers' in collections:
            print("La collection Passengers existe.")

    # Vérifier l'insertion des données
    passengers = collection.find()
    print("Tous les passagers:")
    for passenger in passengers:
        print(passenger)

if __name__ == "__main__":
    create_database_and_collection()
    insert_data()  # Vous pouvez commenter cette ligne après l'importation initiale des données
    analyze_data()
    update_data()
    complex_queries()
    delete_data()
    bulk_update()
    conditional_delete()
    regex_query()
    validate()
