# Enregistrement Étudiant

Ce projet permet de gérer l’enregistrement des étudiants dans une base de données SQL. Il permet de créer, lire, mettre à jour et supprimer des informations sur les étudiants.

## Fonctionnalités

- Ajout d’un nouvel étudiant
- Consultation de la liste des étudiants
- Modification des informations d’un étudiant
- Suppression d’un étudiant
- Requêtes SQL optimisées

## Prérequis

- SGBD compatible  SQL de préférence MySQL 
- Outil de gestion de base de données (ex : phpMyAdmin, DBeaver)
- Accès à un terminal ou une interface SQL
- Avoir docker  installé (optionnel)

## Installation

1. Clonez ce dépôt :

```bash
    git clone git@github.com:tresor-del/enre_etudiant.git
```
2. Configurez la connexion à la base selon vos paramètres.


### Lancer manuellement

1. Backend: 

    ```bash
        cd backend
        # Créer un environnement virtuel avec uv (optionnel) et l'activer 
        uv venv .venv && source .venv/bin/activate
        # Installer les dépendances
        uv pip install -r requirements.txt
        # Lancer l'application
        uvicorn app.main:app --reload
    ```

2. Frontend: 

    ```bash
        cd frontend 
        npm run dev
    ```

3. Tests:

    ```bash
        cd backend
        pytest app/test_main.py
    ```


## Utilisation

Vous devez avoir une base de donnée SQL local pour utiliser l'application. Le code d'interaction avec la base de donnée est dans le  fichier `./backend/app/database/db_utils.py`

L'application est constitué de deux parties: frontend et backend. Vous devez adapter les requêtes SQL a votre base de donnée et même créer un fichier .env pour pouvoir charger les variables d'environnement. Les fichiers de configuration de la base de donnée sont dans le dossier `./backend/app/database`

## Structure du projet

- `backend` :  Dossier du backend avec FastAPI
- `frontend` : Dossier du frontend avec React

## Auteurs

- Tresor

## Licence

Ce projet est sous licence MIT.