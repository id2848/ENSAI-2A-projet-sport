from typing import List, Optional
from business_object.utilisateur import Utilisateur

class UtilisateurDAO:
     def creer(self, utilisateur: Utilisateur) -> bool: 
        """Creation d'un utilisateur dans la base de données

        Parameters
        ----------
        utilisateur : Utilisateur

        Returns
        -------
        created : bool
            True si la création est un succès
            False sinon
        """
          res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO utilisateur(pseudo, mot_de_passe_hash, nom, prenom, date_de_naissance, sexe) VALUES        "
                        "(%(pseudo)s, %(mot_de_passe_hash)s, %(nom)s, %(prenom)s, %(date_de_naissance)s, %(sexe)s)             "
                        "  RETURNING id_utilisateur;                                                ",
                        {
                            "pseudo": utilisateur.pseudo,
                            "mot_de_passe_hash": utilisateur.mot_de_passe_hash,
                            "nom": utilisateur.nom,
                            "prenom": utilisateur.prenom,
                            "date_de_naissance": utilisateur.date_de_naissance,
                            "sexe": utilisateur.sexe,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        created = False
        if res:
            utilisateur.id_utilisateur = res["id_utilisateur"]
            created = True

        return created
    @log
    def trouver_par_id(self, id_utilisateur) -> Utilisateur:
        """trouver un utilisateur grace à son id

        Parameters
        ----------
        id_utilisateur : int
            numéro id de l'utilisateur que l'on souhaite trouver

        Returns
        -------
        utilisateur : Utilisateur
            renvoie l'utilisateur' que l'on cherche par id
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                           "
                        "  FROM utilisateur                      "
                        " WHERE id_utilisateur= %(id_utilisateur)s;  ",
                        {"id_utilisateur": id_utilisateur},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
            raise

        utilisateur = None
        if res:
            utilisateur = Utilisateur(
                pseudo=res["pseudo"],
                nom=res["nom"]
                prenom=res["prenom"]
                date_de_naissance=res["date_de_naissance"],
                sexe=res["sexe"],
                id_utilisateur=res["id_utilisateur"],
            )

        return utilisateur

         @log
    def lister_tous(self) -> list[Utilisateur]:
        """lister tous les utilisateurs

        Parameters
        ----------
        None

        Returns
        -------
        liste_utilisateurs : list[Utilisateur]
            renvoie la liste de tous les joueurs dans la base de données
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                              "
                        "  FROM utilisateur;                        "
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)
            raise

        liste_utilisateurs = []

        if res:
            for row in res:
                utilisateur = Utilisateur(
                    id_utilisateur=row["id_utilisateur"],
                    pseudo=row["pseudo"],
                    mot_de_passe_hash=row["mot_de_passe_hash"],
                    nom=row["nom"],
                    prenom=row["prenom"]
                    date_de_naissance=row["date_de_naissance"],
                    sexe=row["sexe"],
                )

                liste_utilisateurs.append(utilisateur)

        return liste_utilisateurs

          @log
    def modifier(self, utilisateur) -> bool:
        """Modification d'un utilisateur dans la base de données

        Parameters
        ----------
        utilisateur : Utilisateur

        Returns
        -------
        created : bool
            True si la modification est un succès
            False sinon
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE utilisateur                                      "
                        "   SET pseudo                     = %(pseudo)s,                   "
                        "       mot_de_passe_hash          = %(mot_de_passe_hash)s,                      "
                        "       nom                        = %(nom)s,                      "
                        "       prenom                     = %(prenom)s,                      "
                        "       date_de_naissance          = %(date_de_naissance)s,                     "
                        "       sexe                       = %(sexe)s               "
                        " WHERE id_utilisateur = %(id_utilisateur)s;                  ",
                        {
                            "pseudo": utilisateur.pseudo,
                            "mot_de_passe_hash": utilisateur.mot_de_passe_hash,
                            "nom": utilisateur.nom,
                            "prenom": utilisateur.prenom,
                            "date_de_naissance": utilisateur.date_de_naissance,
                            "sexe": utilisateur.sexe
                            "id_utilisateur": utilisateur.id_utilisateur,
                        },
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)

        return res == 1

    @log
   def supprimer(self, utilisateur) -> bool:
        """Suppression d'un utilisateur dans la base de données

        Parameters
        ----------
        utilisateur : Utilisateur
            utilisateur à supprimer de la base de données

        Returns
        -------
            True si l'utilisateur a bien été supprimé
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Supprimer le compte d'un utilisateur
                    cursor.execute(
                        "DELETE FROM utilisateur                  "
                        " WHERE id_utilisateur=%(id_utilisateur)s      ",
                        {"id_utilisateur": utilisateur.id_utilisateur},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)
            raise

        return res > 0

   @log
    def se_connecter(self, pseudo, mot_de_passe_hash) -> Utilisateur:
        """se connecter grâce à son pseudo et son mot de passe

        Parameters
        ----------
        pseudo : str
            pseudo de l'utilisateur que l'on souhaite trouver
        mot_de_passe_hash : str
            mot de passe de l'utilisateur

        Returns
        -------
        utilisateur : Utilisateur
            renvoie l'utilisateur' que l'on cherche
        """
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                           "
                        "  FROM utilisateur                      "
                        " WHERE pseudo = %(pseudo)s         "
                        "   AND mot_de_passe_hash = %(mot_de_passe_hash)s;              ",
                        {"pseudo": pseudo, "mot_de_passe_hash": mot_de_passe_hash},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        utilisateur = None

        if res:
            utilisateur = Utilisateur(
                pseudo=res["pseudo"],
                mot_de_passe_hash=res["mot_de_passe_hash"],
                nom=res["nom"],
                prenom=res["prenom"],
                date_de_naissance=res["date_de_naissance"]
                sexe=res["sexe"],
                id_utilisateur=res["id_utilisateur"],
            )

        return utilisateur

   
