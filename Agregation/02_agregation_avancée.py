from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient('localhost', 27017)
db = client['ventesDB']
collection_clients = db['clients']

def insert_data():
    """Insérer les données des clients et commandes (exemple de données)"""
    clients_data = [
        {
            "clientId": 1,
            "name": "Alice",
            "orders": [
                {"amount": 250, "products": ["product1", "product2", "product3"]},
                {"amount": 450, "products": ["product2", "product4"]}
            ]
        },
        {
            "clientId": 2,
            "name": "Bob",
            "orders": [
                {"amount": 150, "products": ["product1"]},
                {"amount": 200, "products": ["product1", "product3"]}
            ]
        },
        # Ajoutez d'autres clients selon le besoin
    ]
    collection_clients.insert_many(clients_data)
    print("Données des clients insérées.")

def total_sales_by_client():
    """Tâche 1: Total des Ventes par Client"""
    pipeline = [
        {"$unwind": "$orders"},
        {"$group": {"_id": "$name", "totalSales": {"$sum": "$orders.amount"}}}
    ]
    result = collection_clients.aggregate(pipeline)
    print("Total des ventes par client:")
    for doc in result:
        print(doc)

def average_products_per_order():
    """Tâche 2: Panier Moyen par Commande"""
    pipeline = [
        {"$unwind": "$orders"},
        {"$group": {"_id": None, "averageProducts": {"$avg": {"$size": "$orders.products"}}}}
    ]
    result = collection_clients.aggregate(pipeline)
    print("Panier moyen par commande:")
    for doc in result:
        print(doc)

def max_order_by_client():
    """Tâche 3: Commande Maxi par Client"""
    pipeline = [
        {"$unwind": "$orders"},
        {"$group": {"_id": "$name", "maxOrder": {"$max": "$orders.amount"}}}
    ]
    result = collection_clients.aggregate(pipeline)
    print("Commande maximum par client:")
    for doc in result:
        print(doc)

def top_3_products():
    """Tâche 4: Répartition de l’Utilisation des Produits"""
    pipeline = [
        {"$unwind": "$orders"},
        {"$unwind": "$orders.products"},
        {"$group": {"_id": "$orders.products", "totalQuantity": {"$sum": 1}}},
        {"$sort": {"totalQuantity": -1}},
        {"$limit": 3}
    ]
    result = collection_clients.aggregate(pipeline)
    print("Top 3 des produits les plus vendus:")
    for doc in result:
        print(doc)

def validate():
    """Validation des opérations"""
    clients = collection_clients.find()
    print("Tous les clients et leurs commandes:")
    for client in clients:
        print(client)

if __name__ == "__main__":
    insert_data()
    total_sales_by_client()
    average_products_per_order()
    max_order_by_client()
    top_3_products()
    validate()
