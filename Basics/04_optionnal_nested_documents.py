from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient('localhost', 27017)
db = client['schoolDB']
collection = db['classes']

def create_database_and_collection():
    """Partie 1: Préparation"""
    # Sélectionner la Base de Données
    db = client['schoolDB']
    print("Base de données sélectionnée: schoolDB")

    # Créer une Collection
    db.create_collection("classes")
    print("Collection créée: classes")

def insert_document():
    """Partie 2: Insertion de Données"""
    # Insérer un document dans la collection `classes`
    document = {
        "className": "Mathematics 101",
        "professor": "John Doe",
        "students": [
            {
                "name": "Charlie",
                "age": 21,
                "grades": {
                    "midterm": 79,
                    "final": 92
                }
            },
            {
                "name": "Dylan",
                "age": 23,
                "grades": {
                    "midterm": 79,
                    "final": 87
                }
            }
        ]
    }
    result = collection.insert_one(document)
    print("Document inséré avec id:", result.inserted_id)

def query_nested_documents():
    """Partie 3: Requêtes sur Documents Imbriqués"""
    # Récupérer tous les documents de la classe où au moins un étudiant a obtenu plus de 85 au `final`
    result = collection.find({"students.grades.final": {"$gt": 85}})
    print("Documents où au moins un étudiant a obtenu plus de 85 au final:")
    for doc in result:
        print(doc)

def update_nested_document():
    """Partie 4: Mise à Jour d'un Document Imbriqué"""
    # Augmenter de 5 points le `final` de Bob dans "Mathematics 101"
    result = collection.update_one(
        {"className": "Mathematics 101", "students.name": "Bob"},
        {"$inc": {"students.$.grades.final": 5}}
    )
    print("Documents mis à jour:", result.modified_count)

def add_and_remove_elements():
    """Partie 5: Ajout et Suppression d'Éléments Imbriqués"""
    # Ajouter un nouvel étudiant nommé "Charlie"
    result = collection.update_one(
        {"className": "Mathematics 101"},
        {"$push": {"students": {"name": "Charlie", "age": 23, "grades": {"midterm": 82, "final": 88}}}}
    )
    print("Élément ajouté:", result.modified_count)

    # Supprimer l'étudiant Alice
    result = collection.update_one(
        {"className": "Mathematics 101"},
        {"$pull": {"students": {"name": "Alice"}}}
    )
    print("Élément supprimé:", result.modified_count)

def aggregation_operations():
    """Partie 6: Agrégations"""
    # Calculer la note moyenne finale des étudiants de "Mathematics 101"
    pipeline = [
        {"$match": {"className": "Mathematics 101"}},
        {"$unwind": "$students"},
        {"$group": {"_id": "$className", "averageFinal": {"$avg": "$students.grades.final"}}}
    ]
    result = collection.aggregate(pipeline)
    print("Note moyenne finale des étudiants de Mathematics 101:")
    for doc in result:
        print(doc)

    # Trouver la note finale maximale des étudiants de "Mathematics 101"
    pipeline = [
        {"$match": {"className": "Mathematics 101"}},
        {"$unwind": "$students"},
        {"$group": {"_id": "$className", "maxFinal": {"$max": "$students.grades.final"}}}
    ]
    result = collection.aggregate(pipeline)
    print("Note finale maximale des étudiants de Mathematics 101:")
    for doc in result:
        print(doc)

def validate():
    """Validation des opérations"""
    # Vérifier la création de la base de données et de la collection
    databases = client.list_database_names()
    print("Bases de données:")
    print(databases)
    if 'schoolDB' in databases:
        print("La base de données schoolDB existe.")
        collections = db.list_collection_names()
        print("Collections dans schoolDB:")
        print(collections)
        if 'classes' in collections:
            print("La collection classes existe.")

    # Vérifier l'insertion des données
    documents = collection.find()
    print("Tous les documents dans classes:")
    for doc in documents:
        print(doc)

if __name__ == "__main__":
    create_database_and_collection()
    insert_document()
    query_nested_documents()
    update_nested_document()
    add_and_remove_elements()
    aggregation_operations()
    validate()
