from typing import List
from datetime import date, datetime, timedelta
import re

from utils.log_decorator import log

from business_object.utilisateur import Utilisateur

from dao.utilisateur_dao import UtilisateurDao
import logging

class UtilisateurService:
    """Classe contenant les méthodes de service d'Utilisateurs"""


    @log
    def inscrire(
        self,
        pseudo: str,
        mot_de_passe: str,
        nom: str,
        prenom: str,
        date_de_naissance: str,
        sexe: str,
    ) -> bool:
        """
        Inscrit un nouvel utilisateur.
        Retourne True si réussite, False en cas d'erreur.
        """

        try:
            # 1) Validations
            if not self.valider_pseudo(pseudo):
                logging.error(f"Pseudo invalide : {pseudo}")
                return False

            if not self.valider_mot_de_passe(mot_de_passe):
                logging.error("Mot de passe invalide.")
                return False

            if not self.valider_nom_prenom(nom, prenom):
                logging.error("Nom ou prénom invalide.")
                return False

            if not self.valider_date_naissance(date_de_naissance):
                logging.error("Date de naissance invalide.")
                return False

            if not self.valider_sexe(sexe):
                logging.error("Sexe invalide.")
                return False

            # 2) Construction objet métier utilisateur
            utilisateur = Utilisateur(
                pseudo=pseudo,
                nom=nom,
                prenom=prenom,
                date_de_naissance=date_de_naissance,
                sexe=sexe,
            )

            # 3) Utiliser la DAO
            resultat = UtilisateurDao().creer(utilisateur, mot_de_passe)

            # creer() renvoie True ou False donc directement retour
            return resultat
        except Exception as e:
            logging.error(f"Erreur lors de la création de l'utilisateur : {e}")
            return False

    @log
    def se_connecter(self, pseudo: str, mot_de_passe: str) -> Utilisateur | None:
        """
        Vérifie identifiants et renvoie un objet Utilisateur ou None.
        """
        try:
            if not pseudo or not mot_de_passe:
                logging.error("Pseudo ou mot de passe manquant.")
                return None

            utilisateur = UtilisateurDao().se_connecter(pseudo, mot_de_passe)

            if utilisateur is None:
                logging.warning(f"Connexion échouée pour pseudo : {pseudo}")
                return None

            return utilisateur

        except Exception as e:
            logging.error(f"Erreur lors de la connexion de l'utilisateur {pseudo} : {e}")
            return None

    def valider_pseudo(self, pseudo: str) -> bool:
        """Valider que le pseudo est valide et unique (entre 5 et 10 caractères)"""
        if len(pseudo) < 5 or len(pseudo) > 10 or not pseudo.isalnum():
            return False
        return not UtilisateurDao().verifier_pseudo_existant(pseudo)

    def valider_mot_de_passe(self, mot_de_passe: str) -> bool:
        """Valider que le mot de passe est assez fort (entre 5 et 10 caractères)"""
        return len(mot_de_passe) >= 5 and len(mot_de_passe) <= 10

    def valider_nom_prenom(self, nom: str, prenom: str) -> bool:
        """Valider que le nom et prénom ne contiennent que des lettres et des espaces"""
        pattern = "^[A-Za-zÀ-ÿ ]+$"  # Autorise les lettres et les espaces
        return bool(re.match(pattern, nom)) and bool(re.match(pattern, prenom))

    def valider_date_naissance(self, date_de_naissance: str) -> bool:
        """Valider que la date de naissance est au format YYYY-MM-DD"""
        try:
            datetime.strptime(date_de_naissance, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def valider_sexe(self, sexe: str) -> bool:
        """Valider que le sexe est homme, femme ou autre autre"""
        return sexe.lower() in ['homme', 'femme', 'autre']


    def lister_utilisateurs(self) -> List[Utilisateur]:
        """ Liste toutes les utilisateurs  """
        try:
            # Recherche des utilisateurs
            liste = UtilisateurDao().lister_tous()

            # Vérification si aucun utilisateur n'est trouvé
            if not liste:
                print(f"Aucun utilisateur trouvé")

            return liste  # Retourne la liste des utilisateurs (peut être vide)
    
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des utilisateurs: {e}")
            return []  # Retourne une liste vide en cas d'erreur


    def trouver_par_id(self, id_utilisateur) -> Utilisateur:
        """Trouver un Utilisateur à partir de son id"""
        try:
            return UtilisateurDao().trouver_par_id(id_utilisateur)
        except Exception as e:
            logging.error(f"Erreur lors de la récupération de l'utilisateur avec l'id {id_utilisateur} : {e}")
            return None


    def trouver_par_pseudo(self, pseudo) -> Utilisateur:
        """Trouver un Utilisateur à partir de son pseudo"""
        try:
            return UtilisateurDao().trouver_par_pseudo(pseudo)
        except Exception as e:
            logging.error(f"Erreur lors de la récupération de l'utilisateur avec pseudo {pseudo} : {e}")
            return None
