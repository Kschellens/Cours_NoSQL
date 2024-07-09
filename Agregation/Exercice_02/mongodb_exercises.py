from pymongo import MongoClient
import csv

# Chemin vers le fichier CSV téléchargé
csv_file_path = 'D:\Cours_NoSQL\Exercice_02/titanic.csv'  # Assurez-vous que le chemin est correct

# Connexion à MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['TitanicDB']

# Création de la collection 'Passengers' dans la base de données 'TitanicDB'
collection = db['Passengers']
print("Base de données et collection Titanic créées avec succès")

# Insertion des données Titanic
with open(csv_file_path, 'r') as file:
    reader = csv.DictReader(file)
    passenger_list = list(reader)
    collection.insert_many(passenger_list)
    print("Données Titanic insérées avec succès")

# Analyse des données Titanic
# Compter le nombre total de passagers
total_passengers = collection.count_documents({})
print("Nombre total de passagers:", total_passengers)

# Trouver combien de passagers ont survécu
survived_passengers = collection.count_documents({ "Survived": "1" })
print("Nombre de passagers ayant survécu:", survived_passengers)

# Trouver le nombre de passagers femmes
female_passengers = collection.count_documents({ "Sex": "female" })
print("Nombre de passagers femmes:", female_passengers)

# Trouver le nombre de passagers avec au moins 3 enfants
passengers_with_children = collection.count_documents({ "SibSp": { "$gte": 3 } })
print("Nombre de passagers avec au moins 3 enfants:", passengers_with_children)

# Mise à jour des données Titanic
# Mettez à jour les documents pour lesquels le port d'embarquement est manquant, en supposant qu'ils sont montés à bord à Southampton
collection.update_many(
    { "Embarked": "" },
    { "$set": { "Embarked": "S" } }
)
print("Ports d'embarquement mis à jour")

# Ajouter un champ 'rescued' avec la valeur 'true' pour tous les passagers qui ont survécu
collection.update_many(
    { "Survived": "1" },
    { "$set": { "rescued": True } }
)
print("Champ 'rescued' ajouté pour les passagers ayant survécu")

# Requêtes complexes Titanic
# Sélectionnez les noms des 10 passagers les plus jeunes
youngest_passengers = collection.find({}, { "Name": 1, "Age": 1 }).sort("Age", 1).limit(10)
print("Les 10 passagers les plus jeunes:")
for passenger in youngest_passengers:
    print(passenger)

# Identifier les passagers qui n'ont pas survécu et qui étaient dans la 2e classe
second_class_non_survivors = collection.find({ "Survived": "0", "Pclass": "2" })
print("Passagers de la 2e classe qui n'ont pas survécu:")
for passenger in second_class_non_survivors:
    print(passenger)

# Suppression de données Titanic
# Supprimer les enregistrements des passagers qui n'ont pas survécu et dont l'âge est inconnu
collection.delete_many({ "Survived": "0", "Age": "" })
print("Enregistrements des passagers qui n'ont pas survécu et dont l'âge est inconnu supprimés")
