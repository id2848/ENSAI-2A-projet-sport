from typing import List
from datetime import date, timedelta

from utils.log_decorator import log

from business_object.utilisateur import Utilisateur

from dao.utilisateur_dao import UtilisateurDao
import logging

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
        date_de_naissance: str | date,
        sexe: str,
    ) -> bool:
        """
        Inscrit un nouvel utilisateur.
        """
        if UtilisateurDao().verifier_pseudo_existant(pseudo):
            raise AlreadyExistsError("Pseudo déjà existant")
        if not (4 <= len(mot_de_passe) <= 32):
            raise ValueError("Mot de passe invalide. Il doit contenir entre 4 et 32 caractères.")

        utilisateur = Utilisateur(
            pseudo=pseudo,
            nom=nom,
            prenom=prenom,
            date_de_naissance=date_de_naissance,
            sexe=sexe,
        )
        return UtilisateurDao().creer(utilisateur, mot_de_passe)


    @log
    def se_connecter(self, pseudo: str, mot_de_passe: str) -> Utilisateur | None:
        """
        Vérifie identifiants et renvoie un objet Utilisateur ou None.
        """
        if not pseudo or not mot_de_passe:
            raise ValueError("Pseudo ou mot de passe manquant.")

        return UtilisateurDao().se_connecter(pseudo, mot_de_passe)

    @log
    def lister_utilisateurs(self) -> List[Utilisateur]:
        """Lister toutes les utilisateurs"""
        return UtilisateurDao().lister_tous() # Retourne la liste des utilisateurs (peut être vide)

    @log
    def trouver_par_id(self, id_utilisateur: int) -> Utilisateur:
        """Trouver un Utilisateur à partir de son id"""
        if not UtilisateurDao().verifier_id_existant(id_utilisateur):
            raise NotFoundError(f"L'utilisateur avec l'id {id_utilisateur} n'existe pas")
        
        return UtilisateurDao().trouver_par_id(id_utilisateur)

    @log
    def trouver_par_pseudo(self, pseudo: str) -> Utilisateur:
        """Trouver un Utilisateur à partir de son pseudo"""
        if not UtilisateurDao().verifier_pseudo_existant(pseudo):
            raise NotFoundError(f"L'utilisateur avec le pseudo {pseudo} n'existe pas")
        
        return UtilisateurDao().trouver_par_pseudo(pseudo)
