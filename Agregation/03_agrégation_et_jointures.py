from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient('localhost', 27017)
db = client['ventesDB']
collection_commandes = db['commandes']
collection_clients = db['clients']

def insert_data():
    """Insertion des Données de Commandes (exemple de données)"""
    commandes_data = [
        {"commandeId": 1, "idClient": 1, "amount": 250, "products": ["product1", "product2", "product3"]},
        {"commandeId": 2, "idClient": 1, "amount": 450, "products": ["product2", "product4"]},
        {"commandeId": 3, "idClient": 2, "amount": 150, "products": ["product1"]},
        {"commandeId": 4, "idClient": 2, "amount": 200, "products": ["product1", "product3"]}
        # Ajoutez d'autres commandes selon le besoin
    ]
    collection_commandes.insert_many(commandes_data)
    print("Données des commandes insérées.")

def basic_aggregations():
    """Partie 2: Agrégations Classiques"""
    # Calculez le montant total des ventes
    pipeline = [
        {"$group": {"_id": None, "totalSales": {"$sum": "$amount"}}}
    ]
    result = collection_commandes.aggregate(pipeline)
    print("Montant total des ventes:")
    for doc in result:
        print(doc)

    # Trouvez le nombre moyen de produits par commande
    pipeline = [
        {"$group": {"_id": None, "averageProducts": {"$avg": {"$size": "$products"}}}}
    ]
    result = collection_commandes.aggregate(pipeline)
    print("Nombre moyen de produits par commande:")
    for doc in result:
        print(doc)

    # Déterminez le montant maximum d'une commande
    pipeline = [
        {"$group": {"_id": None, "maxOrder": {"$max": "$amount"}}}
    ]
    result = collection_commandes.aggregate(pipeline)
    print("Montant maximum d'une commande:")
    for doc in result:
        print(doc)

def join_clients_orders():
    """Partie 3: Jointure avec la Collection Clients"""
    pipeline = [
        {
            "$lookup": {
                "from": "clients",
                "localField": "idClient",
                "foreignField": "clientId",
                "as": "clientInfo"
            }
        },
        {"$unwind": "$clientInfo"},
        {
            "$project": {
                "_id": 0,
                "commandeId": 1,
                "amount": 1,
                "products": 1,
                "clientName": "$clientInfo.name"
            }
        }
    ]
    result = collection_commandes.aggregate(pipeline)
    print("Détails des commandes avec informations sur les clients:")
    for doc in result:
        print(doc)

def complex_aggregations():
    """Partie 4: Agrégations Plus Complexes"""
    # Calculez le montant total des commandes par client
    pipeline = [
        {"$group": {"_id": "$idClient", "totalAmount": {"$sum": "$amount"}}}
    ]
    result = collection_commandes.aggregate(pipeline)
    print("Montant total des commandes par client:")
    for doc in result:
        print(doc)

    # Identifiez le produit le plus vendu
    pipeline = [
        {"$unwind": "$products"},
        {"$group": {"_id": "$products", "totalSold": {"$sum": 1}}},
        {"$sort": {"totalSold": -1}},
        {"$limit": 1}
    ]
    result = collection_commandes.aggregate(pipeline)
    print("Produit le plus vendu:")
    for doc in result:
        print(doc)

    # Trouvez le client ayant effectué le plus grand nombre de commandes
    pipeline = [
        {"$group": {"_id": "$idClient", "totalOrders": {"$sum": 1}}},
        {"$sort": {"totalOrders": -1}},
        {"$limit": 1}
    ]
    result = collection_commandes.aggregate(pipeline)
    print("Client avec le plus grand nombre de commandes:")
    for doc in result:
        print(doc)

    # Trouvez le client ayant commandé le plus grand nombre de produits
    pipeline = [
        {"$unwind": "$products"},
        {"$group": {"_id": "$idClient", "totalProducts": {"$sum": 1}}},
        {"$sort": {"totalProducts": -1}},
        {"$limit": 1}
    ]
    result = collection_commandes.aggregate(pipeline)
    print("Client ayant commandé le plus grand nombre de produits:")
    for doc in result:
        print(doc)

def validate():
    """Validation des opérations"""
    commandes = collection_commandes.find()
    print("Toutes les commandes:")
    for commande in commandes:
        print(commande)

if __name__ == "__main__":
    insert_data()
    basic_aggregations()
    join_clients_orders()
    complex_aggregations()
    validate()
