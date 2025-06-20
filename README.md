# Logement Backend - Microservices Architecture

Une plateforme de location immobilière construite avec une architecture microservices utilisant Django REST Framework.

## 🏗️ Architecture

Le projet est organisé en microservices indépendants :

- **users_service** : Gestion des utilisateurs et authentification JWT
- **maison_service** : Gestion des propriétés et maisons
- **chambre_service** : Gestion des chambres (rattachées à une maison)

## 📁 Structure du Projet

```
logement_backend/
├── users_service/          # Microservice de gestion des utilisateurs
│   ├── users/             # App Django pour les utilisateurs
│   ├── users_api/         # Configuration Django du service
│   ├── docker-compose.yml # Configuration Docker
│   ├── Dockerfile         # Image Docker
│   └── requirements.txt   # Dépendances Python
├── maison_service/        # Microservice de gestion des maisons
│   ├── maisons/          # App Django pour les maisons
│   ├── maison_service/   # Configuration Django du service
│   ├── docker-compose.yml # Configuration Docker
│   ├── Dockerfile        # Image Docker
│   └── requirements.txt  # Dépendances Python
├── chambre_service/       # Microservice de gestion des chambres
└── README.md             # Ce fichier
```

## 🚀 Services

### Users Service

**Port :** 8000  
**Base de données :** PostgreSQL  
**Documentation :** http://localhost:8000/user/

#### Fonctionnalités :
- Gestion des utilisateurs (création, modification, suppression)
- Authentification JWT
- Génération de tokens d'accès et de rafraîchissement
- API REST sécurisée

#### Endpoints principaux :
- `POST /api/users/` - Créer un utilisateur
- `GET /api/users/` - Liste des utilisateurs
- `POST /api/token/` - Obtenir un token JWT
- `POST /api/token/refresh/` - Rafraîchir un token

### Maison Service

**Port :** 8001  
**Base de données :** PostgreSQL  
**Documentation :** http://localhost:8001/maison/

#### Fonctionnalités :
- Gestion des maisons (CRUD complet)
- Authentification JWT intégrée
- Permissions basées sur le propriétaire
- Validation des coordonnées géographiques
- API REST sécurisée

#### Endpoints principaux :
- `POST /api/maisons/` - Créer une maison
- `GET /api/maisons/` - Liste des maisons du propriétaire
- `GET /api/maisons/{id}/` - Détail d'une maison
- `PUT /api/maisons/{id}/` - Modifier une maison
- `DELETE /api/maisons/{id}/` - Supprimer une maison
- `POST /api/maisons/create_test_user/` - Créer un utilisateur de test
- `POST /api/maisons/get_test_token/` - Obtenir un token de test

### Chambre Service

**Port :** 8002  
**Base de données :** PostgreSQL  
**Documentation :** http://localhost:8002/chambre/

#### Fonctionnalités :
- Gestion des chambres (CRUD complet)
- Chaque chambre appartient à une maison (maison_id)
- Authentification JWT (compatible users_service)
- Permissions : seuls les propriétaires peuvent gérer leurs chambres
- Recherche publique de chambres disponibles avec filtres (type, prix, taille, etc.)
- Validation du type, du prix et du format de la taille
- API REST sécurisée

#### Endpoints principaux :
- `POST /api/chambres/` - Ajouter une chambre à une maison
- `GET /api/chambres/` - Lister les chambres du propriétaire connecté
- `GET /api/chambres/{id}/` - Détail d'une chambre
- `PUT/PATCH /api/chambres/{id}/` - Modifier une chambre
- `DELETE /api/chambres/{id}/` - Supprimer une chambre
- `GET /api/chambres/search/` - Rechercher des chambres disponibles (public)

#### Exemple de création de chambre (curl)
```bash
curl -X POST http://localhost:8002/api/chambres/ \
  -H "Authorization: Bearer VOTRE_TOKEN_JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "maison_id": 1,
    "titre": "Chambre lumineuse",
    "description": "Chambre avec balcon",
    "taille": "15m²",
    "type": "simple",
    "meublee": true,
    "salle_de_bain": true,
    "prix": "350.00",
    "disponible": true
  }'
```

#### Exemple de recherche publique
```bash
curl -X GET "http://localhost:8002/api/chambres/search/?type=simple&prix_max=400"
```

## 🛠️ Installation et Démarrage

### Prérequis
- Docker et Docker Compose
- Git

### 1. Cloner le projet
```bash
git clone <repository-url>
cd logement_backend
```

### 2. Démarrer chaque service
```bash
cd users_service && docker-compose up -d
cd ../maison_service && docker-compose up -d
cd ../chambre_service && docker-compose up -d
```

### 3. Appliquer les migrations
```bash
# Pour chaque service
cd users_service && docker-compose run web python manage.py migrate
cd ../maison_service && docker-compose run web python manage.py migrate
cd ../chambre_service && docker-compose run web python manage.py migrate
```

## 🔐 Authentification

### Générer un token de test
```bash
# Créer un utilisateur de test et obtenir un token
curl -X POST http://localhost:8001/api/maisons/create_test_user/
```

### Utiliser le token
```bash
# Exemple : créer une maison
curl -X POST http://localhost:8001/api/maisons/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer VOTRE_TOKEN_JWT" \
  -d '{
    "adresse": "123 Rue de la Paix, Paris",
    "latitude": 48.8566,
    "longitude": 2.3522,
    "description": "Belle maison avec jardin"
  }'
```

## 📊 Modèles de Données

### User (users_service)
- `id` (auto)
- `username` (string)
- `email` (string)
- `password` (string, hashé)
- `first_name` (string)
- `last_name` (string)
- `date_joined` (datetime)

### Maison (maison_service)
- `id` (auto)
- `proprietaire_id` (integer, référence utilisateur)
- `adresse` (string)
- `latitude` (float)
- `longitude` (float)
- `description` (text)
- `cree_le` (datetime)

## 🔧 Configuration

### Variables d'environnement
Les services utilisent des variables d'environnement pour la configuration :

#### Users Service
- `POSTGRES_DB`: users_db
- `POSTGRES_USER`: users_user
- `POSTGRES_PASSWORD`: users_pass

#### Maison Service
- `POSTGRES_DB`: maison_db
- `POSTGRES_USER`: maison_user
- `POSTGRES_PASSWORD`: maison_pass

### Ports
- Users Service : 8000
- Maison Service : 8001
- Chambre Service : 8002
- PostgreSQL Users : 5432
- PostgreSQL Maison : 5433

## 🧪 Tests

### Tester l'API Users
```bash
# Créer un utilisateur
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

### Tester l'API Maisons
```bash
# Obtenir un token
curl -X POST http://localhost:8001/api/maisons/create_test_user/

# Créer une maison (avec le token obtenu)
curl -X POST http://localhost:8001/api/maisons/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer VOTRE_TOKEN" \
  -d '{
    "adresse": "123 Rue de la Paix, Paris",
    "latitude": 48.8566,
    "longitude": 2.3522,
    "description": "Belle maison avec jardin"
  }'
```

### Tester l'API Chambres
```bash
# Obtenir un token
curl -X POST http://localhost:8002/api/chambres/ \
  -H "Authorization: Bearer VOTRE_TOKEN_JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "maison_id": 1,
    "titre": "Chambre lumineuse",
    "description": "Chambre avec balcon",
    "taille": "15m²",
    "type": "simple",
    "meublee": true,
    "salle_de_bain": true,
    "prix": "350.00",
    "disponible": true
  }'
```

## 📚 Documentation API

- **Users Service :** http://localhost:8000/user/
- **Maison Service :** http://localhost:8001/maison/
- **Chambre Service :** http://localhost:8002/chambre/

## 🐳 Docker

### Commandes utiles
```bash
# Voir les logs
docker-compose logs -f

# Redémarrer un service
docker-compose restart web

# Arrêter tous les services
docker-compose down

# Reconstruire les images
docker-compose build --no-cache
```

## 🔒 Sécurité

- Authentification JWT obligatoire pour toutes les opérations sensibles
- Permissions basées sur le propriétaire pour les maisons et chambres
- Validation des coordonnées géographiques et des formats
- Tokens avec expiration automatique
- Communication sécurisée entre microservices

## 🚀 Déploiement

### Production
1. Modifier les variables d'environnement pour la production
2. Configurer les secrets et clés JWT
3. Utiliser un reverse proxy (nginx)
4. Configurer HTTPS
5. Mettre en place la surveillance et les logs

### Développement
1. Cloner le repository
2. Démarrer les services avec Docker Compose
3. Appliquer les migrations
4. Accéder aux documentations Swagger

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 📞 Support

Pour toute question ou problème :
- Ouvrir une issue sur GitHub
- Consulter la documentation Swagger des services
- Vérifier les logs Docker pour le débogage 