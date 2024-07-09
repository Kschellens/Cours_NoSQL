from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient('localhost', 27017)
db = client['restaurantDB']
collection_commandes = db['commandes']
collection_stocks = db['stocks']

def insert_data():
    """Partie 1 : Insertion des commandes et des stocks (exemple de données)"""
    commandes_data = [
        {
            "idCommande": "C001",
            "idClient": 1,
            "montant": 150,
            "produits": [
                {"nom": "Produit 1", "quantite": 1, "prix": 50},
                {"nom": "Produit 2", "quantite": 2, "prix": 50}
            ]
        },
        {
            "idCommande": "C002",
            "idClient": 1,
            "montant": 90,
            "produits": [
                {"nom": "Produit 3", "quantite": 1, "prix": 90}
            ]
        },
        # Ajoutez d'autres commandes selon le besoin
    ]
    stocks_data = [
        {"ingredientId": 1, "name": "Tomato", "quantity": 100},
        {"ingredientId": 2, "name": "Lettuce", "quantity": 150},
        {"ingredientId": 3, "name": "Chicken", "quantity": 50}
        # Ajoutez d'autres stocks selon le besoin
    ]
    collection_commandes.insert_many(commandes_data)
    collection_stocks.insert_many(stocks_data)
    print("Données des commandes et stocks insérées.")

def update_stock(order):
    """Partie 2 : Mise à jour des stocks à chaque commande"""
    for produit in order['produits']:
        collection_stocks.update_one(
            {"name": produit['nom']},
            {"$inc": {"quantity": -produit['quantite']}}
        )

def alert_low_stock():
    """Partie 3 : Alerter l'utilisateur en cas de niveau de stock bas"""
    low_stocks = collection_stocks.find({"quantity": {"$lt": 10}})
    for stock in low_stocks:
        print(f"Alerte: Stock bas pour {stock['name']} - Quantité restante: {stock['quantity']}")

def analyze_consumption_trends():
    """Partie 4 : Analyse des tendances de consommation"""
    pipeline = [
        {"$unwind": "$produits"},
        {"$group": {"_id": "$produits.nom", "totalQuantity": {"$sum": "$produits.quantite"}}},
        {"$sort": {"totalQuantity": -1}}
    ]
    result = collection_commandes.aggregate(pipeline)
    print("Tendances de consommation:")
    for doc in result:
        print(doc)

def main_menu():
    """Partie 5 : Menu principal de l'application"""
    while True:
        print("\nMenu Principal")
        print("1. Nouvelle commande")
        print("2. Voir les stocks")
        print
