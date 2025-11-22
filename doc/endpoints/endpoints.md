# **Documentation des Endpoints de l'API**

Cette documentation présente de manière synthétique l'ensemble des endpoints implémentés.

---

# **Authentification**

---

### `GET /me`

* **Description** : Récupère le profil de l'utilisateur authentifié.
* **Paramètres** :

  * Authentification Basic requise.
* **Réponse** :

  * `200 OK` : Renvoie les informations de l'utilisateur.

---

### `GET /logout`

* **Description** : Déconnecte l'utilisateur.
* **Réponse** :

  * `401 Unauthorized` : Message de déconnexion.

---

### `POST /inscription`

* **Description** : Crée un nouveau compte utilisateur.
* **Paramètres** (query / form data) :

  * `pseudo` (string)
  * `mot_de_passe` (string)
  * `nom` (string)
  * `prenom` (string)
  * `date_de_naissance` (string, format `YYYY-MM-DD`)
  * `sexe` (string)
* **Réponse** :

  * `200 OK` : Utilisateur inscrit.
  * `400 Bad Request` : Paramètre invalide.
  * `409 Conflict` : Pseudo déjà existant.

---

# **Activités**

---

### `POST /activites`

* **Description** : Crée une nouvelle activité à partir d'un fichier GPX pour l'utilisateur connecté.
* **Paramètres** :

  * `file` (file, obligatoire) : Fichier GPX à uploader
  * `sport` (string, défaut : `"randonnée"`)
* **Réponse** :

  * `200 OK` : Activité créée avec ses détails.
  * `400 Bad Request` : Erreur parsing GPX ou données invalides.
  * `404 Not Found` : Utilisateur non trouvé.

---

### `PUT /activites/{id_activite}`

* **Description** : Modifie une activité existante de l'utilisateur connecté.
* **Paramètres** :

  * `id_activite` (int, path)
  * `sport` (string)
* **Réponse** :

  * `200 OK` : Activité modifiée.
  * `403 Forbidden` : L'activité n'appartient pas au user.
  * `404 Not Found` : Activité introuvable.
  * `400 Bad Request` : Sport invalide.

---

### `DELETE /activites/{id_activite}`

* **Description** : Supprime une activité appartenant à l'utilisateur connecté.
* **Paramètres** :

  * `id_activite` (int)
* **Réponse** :

  * `200 OK` : Activité supprimée.
  * `403 Forbidden` : L'activité ne vous appartient pas.
  * `404 Not Found` : Activité introuvable.

---

### `GET /activites/{id_utilisateur}`

* **Description** : Liste les activités d'un utilisateur.
* **Paramètres** :

  * `id_utilisateur` (int)
* **Réponse** :

  * `200 OK` : Liste des activités.
  * `404 Not Found` : Utilisateur inconnu.

---

### `GET /activites-filtres/{id_utilisateur}`

* **Description** : Liste les activités d'un utilisateur avec filtres optionnels.
* **Paramètres** :

  * `id_utilisateur` (int)
  * `sport` (string, facultatif)
  * `date_debut` (string, format `YYYY-MM-DD`, facultatif)
  * `date_fin` (string, format `YYYY-MM-DD`, facultatif)
* **Réponse** :

  * `200 OK` : Liste filtrée.
  * `404 Not Found` : Utilisateur inconnu.
  * `400 Bad Request` : Format de date invalide.

---

# **Utilisateurs**

---

### `GET /utilisateurs/{id_utilisateur}`

* **Description** : Récupère un utilisateur par son identifiant.
* **Paramètres** :

  * `id_utilisateur` (int)
* **Réponse** :

  * `200 OK` : Informations utilisateur.
  * `404 Not Found` : Utilisateur introuvable.

---

### `GET /utilisateurs/pseudo/{pseudo}`

* **Description** : Récupère un utilisateur à partir de son pseudo.
* **Paramètres** :

  * `pseudo` (string)
* **Réponse** :

  * `200 OK` : Utilisateur.
  * `404 Not Found` : Pseudo inconnu.

---

### `GET /utilisateurs`

* **Description** : Liste tous les utilisateurs inscrits.
* **Réponse** :

  * `200 OK` : Liste des utilisateurs.

---

# **Jaimes**

---

### `POST /jaimes`

* **Description** : Ajoute un "jaime" à une activité pour l'utilisateur connecté.
* **Paramètres** :

  * `id_activite` (int)
* **Réponse** :

  * `200 OK` : Jaime ajouté.
  * `404 Not Found` : Activité introuvable.
  * `409 Conflict` : Jaime déjà existant.

---

### `DELETE /jaimes/{id_activite}`

* **Description** : Supprime le jaime de l'utilisateur pour une activité.
* **Paramètres** :

  * `id_activite` (int)
* **Réponse** :

  * `200 OK` : Jaime supprimé.
  * `404 Not Found` : Jaime introuvable.

---

### `GET /jaimes/existe`

* **Description** : Vérifie si un jaime existe entre un utilisateur et une activité.
* **Paramètres** :

  * `id_activite` (int)
  * `id_auteur` (int)
* **Réponse** :

  * `200 OK` : Booléen jaime présent ou non.
  * `404 Not Found` : Activité ou utilisateur introuvable.

---

### `GET /jaimes/compter`

* **Description** : Compte le nombre de jaimes d'une activité.
* **Paramètres** :

  * `id_activite` (int)
* **Réponse** :

  * `200 OK` : Nombre de jaimes.
  * `404 Not Found` : Activité introuvable.

---

# **Commentaires**

---

### `POST /commentaires`

* **Description** : Ajoute un commentaire à une activité.
* **Paramètres** :

  * `id_activite` (int)
  * `commentaire` (string)
* **Réponse** :

  * `200 OK` : Commentaire ajouté.
  * `404 Not Found` : Activité introuvable.

---

### `DELETE /commentaires/{id_commentaire}`

* **Description** : Supprime un commentaire appartenant à l'utilisateur connecté.
* **Paramètres** :

  * `id_commentaire` (int)
* **Réponse** :

  * `200 OK` : Commentaire supprimé.
  * `403 Forbidden` : Le commentaire ne vous appartient pas.
  * `404 Not Found` : Commentaire introuvable.

---

### `GET /commentaires/{id_activite}`

* **Description** : Liste les commentaires d'une activité.
* **Paramètres** :

  * `id_activite` (int)
* **Réponse** :

  * `200 OK` : Liste des commentaires.
  * `404 Not Found` : Activité inconnue.

---

# **Abonnements**

---

### `POST /abonnements`

* **Description** : L'utilisateur connecté s'abonne à un autre utilisateur.
* **Paramètres** :

  * `id_utilisateur_suivi` (int)
* **Réponse** :

  * `200 OK` : Abonnement créé.
  * `409 Conflict` : Abonnement déjà existant.
  * `404 Not Found` : Utilisateur introuvable.

---

### `DELETE /abonnements`

* **Description** : Se désabonner d'un utilisateur.
* **Paramètres** :

  * `id_utilisateur_suivi` (int)
* **Réponse** :

  * `200 OK` : Abonnement supprimé.
  * `404 Not Found` : Abonnement inexistant.

---

### `GET /abonnements/existe`

* **Description** : Vérifie si un abonnement existe entre deux utilisateurs.
* **Paramètres** :

  * `id_utilisateur_suiveur` (int)
  * `id_utilisateur_suivi` (int)
* **Réponse** :

  * `200 OK` : Booléen.
  * `404 Not Found` : Un des utilisateurs n'existe pas.

---

### `GET /abonnements/suivis/{id_utilisateur}`

* **Description** : Liste les utilisateurs suivis par un utilisateur donné.
* **Paramètres** :

  * `id_utilisateur` (int)
* **Réponse** :

  * `200 OK` : Liste des suivis.
  * `404 Not Found` : Utilisateur inconnu.

---

### `GET /abonnements/suiveurs/{id_utilisateur}`

* **Description** : Liste les abonnés d'un utilisateur.
* **Paramètres** :

  * `id_utilisateur` (int)
* **Réponse** :

  * `200 OK` : Liste des suiveurs.
  * `404 Not Found` : Utilisateur introuvable.

---

# **Fil d'actualité**

---

### `GET /fil-dactualite/{id_utilisateur}`

* **Description** : Renvoie le fil d'actualités de l'utilisateur (activités des suivis).
* **Paramètres** :

  * `id_utilisateur` (int)
* **Réponse** :

  * `200 OK` : Fil d'actualité.
  * `404 Not Found` : Utilisateur introuvable.

---

# **Statistiques**

---

### `GET /statistiques/total/{id_utilisateur}`

* **Description** : Récupère les statistiques globales d'un utilisateur.
* **Paramètres** :

  * `id_utilisateur` (int)
* **Réponse** :

  * `200 OK` : Nombre total d'activités, distance totale, durée totale.
  * `404 Not Found` : Utilisateur inconnu.

---

### `GET /statistiques/semaine/{id_utilisateur}`

* **Description** : Récupère les statistiques d'une semaine donnée.
* **Paramètres** :

  * `id_utilisateur` (int)
  * `date_reference` (string, format `YYYY-MM-DD`)
* **Réponse** :

  * `200 OK` : Activités, distance et durée de la semaine.
  * `404 Not Found` : Utilisateur inconnu.
  * `400 Bad Request` : Format de date invalide.

---

# **Utilitaires**

---

### `POST /upload-gpx`

* **Description** : Upload et parsing d'un fichier GPX.
* **Paramètres** :

  * `file` (file)
* **Réponse** :

  * `200 OK` : Résultat du parsing.
  * `400 Bad Request` : Fichier GPX invalide.
