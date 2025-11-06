# Liste des endpoints

Ce fichier présente les différents endpoints à implémenter dans l'API.

---

## Authentification

### `POST /login`
- **Description** : Authentifie un utilisateur avec un nom d'utilisateur et un mot de passe via HTTP Basic Auth.
- **Paramètres** : 
  - `username` (string) : Nom d'utilisateur
  - `password` (string) : Mot de passe
- **Réponse** :
  - `200 OK` si authentifié.
  - `401 Unauthorized` si non.

### `GET /me`
- **Description** : Récupère les informations de l'utilisateur actuellement connecté.
- **Réponse** : 
  - Informations de l'utilisateur.
  
### à compléter

---

## Gestion des activités

### `GET /activites/{id_utilisateur}`
- **Description** : Liste toutes les activités d'un utilisateur donné.
- **Paramètres** : 
  - `id_utilisateur` (int) : ID de l'utilisateur
- **Réponse** : 
  - Liste des objets `Activite` (sport, date, distance, durée).

### `POST /activites`
- **Description** : Crée une nouvelle activité à partir d'un fichier GPX.
- **Paramètres** : 
  - `file` (file) : Fichier GPX à uploader
  - `sport` (string) : Type de sport
- **Réponse** : 
  - `201 Created` si l'activité est créée, avec les détails de l'activité.

### `PUT /activites/{id_activite}`
- **Description** : Modifie une activité existante.
- **Paramètres** : 
  - `id_activite` (int) : ID de l'activité
  - `sport` (string) : Type de sport à modifier
- **Réponse** : 
  - `200 OK` si mise à jour réussie
  - `404 Not Found` si l'activité n'est pas trouvée.

### `DELETE /activites/{id_activite}`
- **Description** : Supprime une activité.
- **Paramètres** : 
  - `id_activite` (int) : ID de l'activité à supprimer
- **Réponse** : 
  - `200 OK` si la suppression est réussie
  - `404 Not Found` si l'activité n'existe pas.

---

## Interactions avec les activités

### `POST /jaimes`
- **Description** : L'utilisateur ajoute un "jaime" à une activité d'un autre utilisateur.
- **Paramètres** : 
  - `id_activite` (int) : ID de l'activité à aimer
  - `id_utilisateur` (int) : ID de l'utilisateur qui aime
- **Réponse** : 
  - `201 OK` si succès.

### `DELETE /jaimes/{id_activite}/{id_utilisateur}`
- **Description** : L'utilisateur supprime son "jaime" d'une activité.
- **Paramètres** : 
  - `id_activite` (int) : ID de l'activité
  - `id_utilisateur` (int) : ID de l'utilisateur
- **Réponse** : 
  - `200 OK` si succès.

### `POST /commentaires`
- **Description** : L'utilisateur ajoute un commentaire à une activité.
- **Paramètres** : 
  - `id_activite` (int) : ID de l'activité
  - `id_utilisateur` (int) : ID de l'utilisateur
  - `commentaire` (string) : Contenu du commentaire
- **Réponse** : 
  - `201 OK` si commentaire ajouté.

### `DELETE /commentaires/{id_commentaire}`
- **Description** : L'utilisateur supprime un commentaire.
- **Paramètres** : 
  - `id_commentaire` (int) : ID du commentaire à supprimer
- **Réponse** : 
  - `200 OK` si suppression réussie.

---

## Abonnements

### `POST /abonnements`
- **Description** : L'utilisateur s'abonne à un autre utilisateur.
- **Paramètres** : 
  - `id_utilisateur_suiveur` (int) : ID de l'utilisateur suiveur
  - `id_utilisateur_suivi` (int) : ID de l'utilisateur suivi
- **Réponse** : 
  - `201 OK` si abonnement réussi.

### `DELETE /abonnements`
- **Description** : L'utilisateur se désabonne d'un autre utilisateur.
- **Paramètres** : 
  - `id_utilisateur_suiveur` (int) : ID de l'utilisateur suiveur
  - `id_utilisateur_suivi` (int) : ID de l'utilisateur suivi
- **Réponse** : 
  - `200 OK` si désabonnement réussi.

### `GET /abonnements/suivis/{id_utilisateur}`
- **Description** : Récupère la liste des utilisateurs suivis par un utilisateur.
- **Paramètres** : 
  - `id_utilisateur` (int) : ID de l'utilisateur
- **Réponse** : 
  - Liste des utilisateurs suivis.

### `GET /abonnements/suiveurs/{id_utilisateur}`
- **Description** : Récupère la liste des utilisateurs qui suivent un utilisateur.
- **Paramètres** : 
  - `id_utilisateur` (int) : ID de l'utilisateur
- **Réponse** : 
  - Liste des utilisateurs suiveurs.

---

## Fil d'actualités

### `GET /fil-dactualite/{id_utilisateur}`
- **Description** : Récupère les activités des utilisateurs suivis dans un fil d'actualité.
- **Paramètres** : 
  - `id_utilisateur` (int) : ID de l'utilisateur
- **Réponse** : 
  - Liste des activités des utilisateurs suivis.

---

## Statistiques

### `GET /statistiques/activites/{id_utilisateur}`
- **Description** : Récupère les statistiques des activités d'un utilisateur.
- **Paramètres** : 
  - `id_utilisateur` (int) : ID de l'utilisateur
- **Réponse** : 
  - Distance totale, durée totale, nombre d'heures d'activités.

### `GET /statistiques/hebdomadaire/{id_utilisateur}`
- **Description** : Récupère les statistiques hebdomadaires détaillées (par sport, distance, durée).
- **Paramètres** : 
  - `id_utilisateur` (int) : ID de l'utilisateur
- **Réponse** : 
  - Par semaine : distance parcourue, nombre d'heures d'activités, nombre d'activités par sport.
