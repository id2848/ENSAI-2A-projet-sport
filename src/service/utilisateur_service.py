from typing import List
from datetime import date, timedelta

from utils.log_decorator import log

from business_object.utilisateur import Utilisateur

from dao.utilisateur_dao import UtilisateurDao
import logging

from utils.verifier_date import verifier_date

from exceptions import NotFoundError, AlreadyExistsError

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
        """

        # --- 1) Validations ---
        if not Utilisateur.valider_pseudo(pseudo):
            raise ValueError("Pseudo invalide. Il doit être alphanumérique et contenir entre 4 et 16 caractères.")

        if UtilisateurDao().verifier_pseudo_existant(pseudo):
            raise AlreadyExistsError("Pseudo déjà existant")

        if not Utilisateur.valider_nom_prenom(nom, prenom):
            raise ValueError("Nom ou prénom invalide")

        if not verifier_date(date_de_naissance):
            raise ValueError("Date de naissance invalide. Utilisez le format YYYY-MM-DD")

        if not Utilisateur.valider_sexe(sexe):
            raise ValueError("Sexe invalide. Il doit être 'homme', 'femme' ou 'autre'")

        if not (4 <= len(mot_de_passe) <= 32):
            raise ValueError("Mot de passe invalide. Il doit contenir entre 4 et 32 caractères.")

        # 2) Construire l'objet utilisateur
        utilisateur = Utilisateur(
            pseudo=pseudo,
            nom=nom,
            prenom=prenom,
            date_de_naissance=date_de_naissance,
            sexe=sexe,
        )

        # 3) DAO
        return UtilisateurDao().creer(utilisateur, mot_de_passe)


    @log
    def se_connecter(self, pseudo: str, mot_de_passe: str) -> Utilisateur | None:
        """
        Vérifie identifiants et renvoie un objet Utilisateur ou None.
        """
        if not pseudo or not mot_de_passe:
            raise ValueError("Pseudo ou mot de passe manquant.")

        return UtilisateurDao().se_connecter(pseudo, mot_de_passe)

    def lister_utilisateurs(self) -> List[Utilisateur]:
        """Lister toutes les utilisateurs"""
        return UtilisateurDao().lister_tous() # Retourne la liste des utilisateurs (peut être vide)

    def trouver_par_id(self, id_utilisateur: int) -> Utilisateur:
        """Trouver un Utilisateur à partir de son id"""
        if not UtilisateurDao().verifier_id_existant(id_utilisateur):
            raise NotFoundError(f"L'utilisateur avec l'id {id_utilisateur} n'existe pas")
        
        return UtilisateurDao().trouver_par_id(id_utilisateur)

    def trouver_par_pseudo(self, pseudo: str) -> Utilisateur:
        """Trouver un Utilisateur à partir de son pseudo"""
        if not UtilisateurDao().verifier_pseudo_existant(pseudo):
            raise NotFoundError(f"L'utilisateur avec le pseudo {pseudo} n'existe pas")
        
        return UtilisateurDao().trouver_par_pseudo(pseudo)
