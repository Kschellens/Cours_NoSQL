from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient('localhost', 27017)
db = client['subwayDB']
collection_commandes = db['commandes']
collection_ingredients = db['ingredients']
collection_sauces = db['sauces']

def insert_ingredients_and_sauces():
    """Partie 1 : Insertion des ingrédients et sauces"""
    ingredients_data = [
        {"ingredientId": 1, "name": "Tomato", "price": 0.5},
        {"ingredientId": 2, "name": "Lettuce", "price": 0.3},
        {"ingredientId": 3, "name": "Chicken", "price": 1.5}
        # Ajoutez d'autres ingrédients selon le besoin
    ]
    sauces_data = [
        {"sauceId": 1, "name": "Mayo", "price": 0.2},
        {"sauceId": 2, "name": "Ketchup", "price": 0.2}
        # Ajoutez d'autres sauces selon le besoin
    ]
    collection_ingredients.insert_many(ingredients_data)
    collection_sauces.insert_many(sauces_data)
    print("Données des ingrédients et sauces insérées.")

def create_order():
    """Partie 2 : Création d'une nouvelle commande"""
    ingredients = [1, 2]  # Ids des ingrédients sélectionnés par l'utilisateur
    sauce = 1  # Id de la sauce sélectionnée par l'utilisateur
    total_price = 0

    # Calcul du prix total des ingrédients
    for ingredient_id in ingredients:
        ingredient = collection_ingredients.find_one({"ingredientId": ingredient_id})
        total_price += ingredient["price"]

    # Ajout du prix de la sauce
    sauce_data = collection_sauces.find_one({"sauceId": sauce})
    total_price += sauce_data["price"]

    # Insertion de la commande dans la collection
    order = {
        "ingredients": ingredients,
        "sauce": sauce,
        "total_price": total_price
    }
    result = collection_commandes.insert_one(order)
    print("Commande créée avec id:", result.inserted_id)

def view_revenue():
    """Partie 3 : Voir le chiffre d'affaires"""
    pipeline = [
        {"$group": {"_id": None, "totalRevenue": {"$sum": "$total_price"}}}
    ]
    result = collection_commandes.aggregate(pipeline)
    for doc in result:
        print("Chiffre d'affaires total:", doc["totalRevenue"])

def main_menu():
    """Partie 4 : Menu principal de l'application"""
    while True:
        print("\nMenu Principal")
        print("1. Nouvelle commande")
        print("2. Voir le chiffre d'affaires")
        print("3. Quitter")
        choice = input("Choisissez une option: ")

        if choice == "1":
            create_order()
        elif choice == "2":
            view_revenue()
        elif choice == "3":
            break
        else:
            print("Option invalide, veuillez réessayer.")

if __name__ == "__main__":
    insert_ingredients_and_sauces()  # Partie 1 : Insertion des ingrédients et sauces
    main_menu()  # Partie 4 : Affichage du menu principal et interaction avec l'utilisateur
