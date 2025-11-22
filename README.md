## ENSAI-2A-Projet-Sport

Projet informatique de 2ème année ENSAI.

Cette application est un **réseau social sportif** permettant aux utilisateurs de gérer leurs activités physiques et d'interagir avec une communauté. Elle repose sur une architecture en couches (DAO, Service, Business Object) et expose une API REST consommée par une interface Web.

Principales fonctionnalités :
- **Import et analyse de fichiers GPX** (calcul de distance, durée, dénivelé, vitesse).
- **Réseau social** : Suivre des amis, fil d'actualité, recherche de profils.
- **Interactions** : Liker et commenter les activités.
- **Statistiques** : Suivi des performances globales et hebdomadaires.
- **Interfaces** : Une interface Web moderne (Streamlit) et une API Backend (FastAPI).

## :arrow_forward: Logiciels et outils

- [Visual Studio Code](https://code.visualstudio.com/)
- [Python 3.13](https://www.python.org/)
- [Git](https://git-scm.com/)
- [PostgreSQL](https://www.postgresql.org/) (Base de données)
- [Streamlit](https://streamlit.io/) (Interface Frontend)
- [FastAPI](https://fastapi.tiangolo.com/) (Backend)

## :arrow_forward: Cloner le dépôt

- [ ] Ouvrir VSCode
- [ ] Ouvrir **Git Bash**
- [ ] Cloner le dépôt :
  - `git clone <VOTRE_URL_GITHUB>`

### Ouvrir le dossier

- [ ] Ouvrir **Visual Studio Code**
- [ ] File > Open Folder
- [ ] Sélectionner le dossier du projet
  - :warning: Assurez-vous d'être à la racine du projet pour que les imports fonctionnent correctement.

## Aperçu des fichiers

| Fichier / Dossier          | Description                                                                 |
| -------------------------- | --------------------------------------------------------------------------- |
| `src/streamlit_app.py`     | **Point d'entrée de l'interface Web** (Frontend).                           |
| `src/app.py`               | **Point d'entrée de l'API** (Backend FastAPI).                              |
| `src/main.py`              | Script de démonstration pour l'analyse locale de fichiers GPX.              |
| `data`                     | Scripts SQL d'initialisation et de population de la base de données.        |
| `doc`                      | Documentation (Endpoints, Diagrammes UML, Planning).                        |
| `requirements.txt`         | Liste des dépendances Python nécessaires.                                   |
| `.env`                     | Variables d'environnement (Configuration BDD, API).                         |

### Fichiers de configuration

Vous n'aurez généralement pas besoin de modifier ces fichiers, sauf le `.env`.

| Fichier                    | Description                                                                 |
| -------------------------- | --------------------------------------------------------------------------- |
| `.gitignore`               | Liste les fichiers ignorés par Git (ex: `.env`, `__pycache__`).             |
| `logging_config.yml`       | Configuration des logs de l'application.                                    |
| `pytest.ini` / `.coveragerc`| Configuration pour les tests unitaires et la couverture de code.           |

## :arrow_forward: Installation des dépendances

- [ ] Dans Git Bash, exécutez les commandes suivantes pour installer les paquets requis :

```bash
pip install -r requirements.txt
pip list
```

## :arrow\_forward: Variables d'environnement

Vous devez définir les variables pour connecter l'application à votre base de données PostgreSQL et configurer le Webservice.

À la racine du projet :

  - [ ] Créez un fichier nommé `.env`
  - [ ] Copiez et adaptez le contenu ci-dessous :

<!-- end list -->

```default
# Configuration de l'API (si nécessaire)
API_HOST=localhost
API_PORT=9876

# Base de données PostgreSQL
POSTGRES_HOST=sgbd-eleves.domensai.ecole
POSTGRES_PORT=5432
POSTGRES_DATABASE=idxxxx
POSTGRES_USER=idxxxx
POSTGRES_PASSWORD=idxxxx
POSTGRES_SCHEMA=projet
```

### Initialiser la base de données

Après avoir créé votre base PostgreSQL et configuré le fichier `.env`, vous devez initialiser la base de données la toute première fois.

Dans un terminal :

```bash
python src/utils/reset_database.py
```


## :arrow\_forward: Lancer l'application

L'application se compose de deux parties qui doivent fonctionner en parallèle : le **Backend** (API) et le **Frontend** (Streamlit).

### 1\. Lancer le Backend (API)

Ce service gère la logique métier, la base de données et l'analyse des fichiers GPX.

  - [ ] Dans un terminal :

<!-- end list -->

```bash
python src/app.py
```

*L'API sera accessible sur `http://localhost:9876`.*

Documentation de l'API (une fois lancée) :

  - Swagger UI : `http://localhost:9876/docs`
  - ReDoc : `http://localhost:9876/redoc`

### 2\. Lancer le Frontend (Streamlit)

C'est l'interface graphique que vous utiliserez dans votre navigateur.

  - [ ] Dans un **nouveau** terminal :

<!-- end list -->

```bash
streamlit run src/streamlit_app.py
```

*Votre navigateur devrait s'ouvrir automatiquement.*
*Si ce n'est pas le cas, ouvrez manuellement l'URL affichée dans le terminal (par défaut : http://localhost:8501).*

## :arrow\_forward: Fonctionnalités détaillées

Une fois sur l'interface Streamlit, vous pouvez :

1.  **Authentification** : Vous inscrire ou vous connecter.
2.  **Fil d'actualité** : Voir les dernières activités des personnes que vous suivez.
3.  **Mes Activités** : Consulter votre historique, voir les détails (vitesse, carte, etc.) et supprimer des activités.
4.  **Poster (GPX)** : Uploader un fichier `.gpx` (ex: export Strava/Garmin). L'application analyse automatiquement la distance, la durée et le dénivelé avant validation.
5.  **Rechercher Profil** : Trouver d'autres utilisateurs par pseudo, visiter leur profil et s'abonner ("Suivre").
6.  **Statistiques** : Visualiser vos totaux (km parcourus, temps total) et vos performances de la semaine.

## :arrow\_forward: Tests Unitaires

Les tests assurent la fiabilité du code (notamment les Services et les DAO).

  - [ ] Lancer les tests : `pytest -v`
  - [ ] Vérifier la couverture :

<!-- end list -->

```bash
coverage run -m pytest
coverage report -m
```

## :arrow\_forward: Logs

Les logs permettent de suivre l'exécution du backend. Ils sont configurés via `logging_config.yml` et visibles dans le terminal où tourne `src/app.py` ou dans le dossier `logs/` (si configuré).

Exemple de log lors d'une connexion :

```
INFO     -         UtilisateurService.se_connecter('johndoe', '*****') - DEBUT
INFO     -             UtilisateurDao.se_connecter('johndoe', '*****') - DEBUT
INFO     -             UtilisateurDao.se_connecter('johndoe', '*****') - FIN
INFO     -                └─> Sortie : Utilisateur(id_utilisateur=991, pseudo='johndoe', nom='Doe', prenom='John', date_de_naissance=datetime.date(1990, 1, 1), sexe='homme')
INFO     -         UtilisateurService.se_connecter('johndoe', '*****') - FIN
INFO     -            └─> Sortie : Utilisateur(id_utilisateur=991, pseudo='johndoe', nom='Doe', prenom='John', date_de_naissance=datetime.date(1990, 1, 1), sexe='homme')
```
