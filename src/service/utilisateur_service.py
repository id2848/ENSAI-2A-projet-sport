from typing import List
from datetime import date, timedelta

from utils.log_decorator import log

from business_object.utilisateur import Utilisateur

from dao.utilisateur_dao import UtilisateurDao
import logging

from utils.verifier_date import verifier_date

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
    ):
        """
        Inscrit un nouvel utilisateur.
        Retourne un dict standardisé :
        { success: bool, result: utilisateur | None, error: message | None }
        """

        try:
            # --- 1) Validations ---
            if not Utilisateur.valider_pseudo(pseudo):
                return {"success": False, "result": None, "error": "Pseudo invalide. Il doit être alphanumérique et contenir entre 4 et 16 caractères."}

            if UtilisateurDao().verifier_pseudo_existant(pseudo):
                return {"success": False, "result": None, "error": "Pseudo déjà existant"}

            if not Utilisateur.valider_nom_prenom(nom, prenom):
                return {"success": False, "result": None, "error": "Nom ou prénom invalide"}

            if not verifier_date(date_de_naissance):
                return {"success": False, "result": None, "error": "Date de naissance invalide. Utilisez le format YYYY-MM-DD"}

            if not Utilisateur.valider_sexe(sexe):
                return {"success": False, "result": None, "error": "Sexe invalide. Il doit être 'homme', 'femme' ou 'autre'"}

            if not (4 <= len(mot_de_passe) <= 32):
                return {"success": False, "result": None, "error": "Mot de passe invalide. Il doit contenir entre 4 et 32 caractères."}

            # 2) Construire l'objet utilisateur
            utilisateur = Utilisateur(
                pseudo=pseudo,
                nom=nom,
                prenom=prenom,
                date_de_naissance=date_de_naissance,
                sexe=sexe,
            )

            # 3) DAO
            creation = UtilisateurDao().creer(utilisateur, mot_de_passe)

            if not creation:
                return {
                    "success": False,
                    "result": None,
                    "error": "Erreur lors de la création en base de données",
                }

            return {
                "success": True,
                "result": utilisateur,
                "error": None,
            }

        except Exception as e:
            logging.error(f"Erreur lors de la création de l'utilisateur : {e}")
            return {
                "success": False,
                "result": None,
                "error": "Erreur interne lors de l'inscription",
            }


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

    def lister_utilisateurs(self) -> List[Utilisateur]:
        """Lister toutes les utilisateurs"""
        try:
            # Recherche des utilisateurs
            liste = UtilisateurDao().lister_tous()

            return liste  # Retourne la liste des utilisateurs (peut être vide)
    
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des utilisateurs: {e}")
            return None


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
