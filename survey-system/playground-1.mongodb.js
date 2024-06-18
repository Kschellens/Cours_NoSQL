// Sélectionner la base de données
use('surveySystem');

// Création des collections (si elles n'existent pas déjà)
db.createCollection('sondages');
db.createCollection('reponses');

// Insertion de données de test dans la collection 'sondages'
db.sondages.insertMany([
  {
    "nom": "Sondage Préférences Alimentaires",
    "createur": ObjectId("5f3a3c1b1234567890123456"),
    "questions": [
      {
        "_id": ObjectId("5f3a3c1d1234567890123456"),
        "intitule": "Quel est votre plat préféré ?",
        "type": "ouverte"
      },
      {
        "_id": ObjectId("5f3a3c1e1234567890123456"),
        "intitule": "Quels types de cuisine préférez-vous ?",
        "type": "qcm",
        "reponses": ["Italienne", "Chinoise", "Mexicaine", "Indienne"]
      }
    ]
  }
]);

// Insertion de données de test dans la collection 'reponses'
db.reponses.insertMany([
  {
    "sondage_id": ObjectId("5f3a3c1c1234567890123456"),
    "utilisateur_id": ObjectId("5f3a3c1d1234567890123456"),
    "reponses": [
      {
        "question_id": ObjectId("5f3a3c1d1234567890123456"),
        "reponse": "Pizza"
      },
      {
        "question_id": ObjectId("5f3a3c1e1234567890123456"),
        "reponse": ["Italienne", "Indienne"]
      }
    ]
  }
]);

// Créer un nouveau sondage
db.sondages.insertOne({
  "nom": "Sondage Loisirs",
  "createur": ObjectId("5f3a3c1b1234567890123457"),
  "questions": [
    {
      "_id": ObjectId(),
      "intitule": "Quel est votre loisir préféré ?",
      "type": "ouverte"
    },
    {
      "_id": ObjectId(),
      "intitule": "Quels sports aimez-vous pratiquer ?",
      "type": "qcm",
      "reponses": ["Football", "Basketball", "Tennis", "Natation"]
    }
  ]
});

// Modifier un sondage existant en ajoutant une nouvelle question
db.sondages.updateOne(
  { "nom": "Sondage Préférences Alimentaires" },
  { $push: { "questions": { "_id": ObjectId(), "intitule": "Quelle est votre boisson préférée ?", "type": "ouverte" } } }
);

// Supprimer un sondage par son nom
db.sondages.deleteOne({ "nom": "Sondage Loisirs" });

// Mettre à jour une question dans un sondage
db.sondages.updateOne(
  { "nom": "Sondage Préférences Alimentaires", "questions.intitule": "Quel est votre plat préféré ?" },
  { $set: { "questions.$.intitule": "Quel est votre dessert préféré ?" } }
);

// Insérer des réponses à un sondage
db.reponses.insertOne({
  "sondage_id": ObjectId("5f3a3c1c1234567890123456"),
  "utilisateur_id": ObjectId("5f3a3c1d1234567890123457"),
  "reponses": [
    {
      "question_id": ObjectId("5f3a3c1d1234567890123456"),
      "reponse": "Cheesecake"
    },
    {
      "question_id": ObjectId("5f3a3c1e1234567890123456"),
      "reponse": ["Mexicaine", "Indienne"]
    }
  ]
});

// Obtenir la liste de tous les sondages
db.sondages.find().pretty();
