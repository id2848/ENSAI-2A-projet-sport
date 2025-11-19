from typing import List
from datetime import date, datetime, timedelta

from utils.log_decorator import log

from business_object.utilisateur import Utilisateur
from business_object.abonnement import Abonnement
from business_object.activite import Activite
from business_object.commentaire import Commentaire
from business_object.jaime import Jaime

from dao.abonnement_dao import AbonnementDao
from dao.utilisateur_dao import UtilisateurDao
from dao.activite_dao import ActiviteDao
from dao.commentaire_dao import CommentaireDao
from dao.jaime_dao import JaimeDao

import logging

class ActiviteService:
    """Classe contenant les méthodes de service des activités Utilisateurs"""

    
    def creer_activite(self, id_utilisateur: int, sport: str, date_activite: date, distance: float, duree: timedelta) -> bool:
        """Crée une nouvelle activité"""
        try:
            activite = Activite(
                id_utilisateur=id_utilisateur,
                sport=sport,
                date_activite=date_activite,  # Utilisation du paramètre `date_activite` passé
                distance=distance,
                duree=duree
            )
            # Simuler l'enregistrement de l'activité dans la base de données
            return ActiviteDao().creer(activite)  # Appel à DAO pour l'enregistrement
        except Exception as e:
            logging.error(f"Erreur lors de la création de l'activité : {e}")  # Affichage de l'erreur pour le diagnostic
            return False
            
    def supprimer_activite(self, id_activite: int) -> bool:
        """Supprime une activité existante"""
        try:
            activite = ActiviteDao().trouver_par_id(id_activite=id_activite)  # Récupère l'activité par son ID
        
            # Si l'activité n'existe pas
            if activite is None:
                logging.warning(f"L'activité avec ID {id_activite} n'existe pas.")
                return False
        
            return ActiviteDao().supprimer(activite=activite)  # Effectue la suppression dans la base de données
        
        except Exception as e:
            logging.error(f"Erreur lors de la suppression de l'activité : {e}")
            return False

    def modifier_activite(self, id_activite: int, sport: str) -> bool:
        """Modifie une activité existante"""
        try:
            activite = ActiviteDao().trouver_par_id(id_activite=id_activite)  # Récupère l'activité par son ID
            # Si l'activité n'existe pas
            if activite is None:
                logging.warning(f"L'activité avec ID {id_activite} n'existe pas.")
                return False
        
            activite.sport = sport  # Modification du sport de l'activité
            return ActiviteDao().modifier(activite)
        
        except Exception as e:
            logging.error(f"Erreur lors de la modification de l'activité : {e}")
            return False
    
    def trouver_activite_par_id(self, id_activite: int):
        """Trouver une activité par son id"""
        try:
            activite = ActiviteDao().trouver_par_id(id_activite=id_activite)
            # Si l'activité n'existe pas
            if activite is None:
                logging.warning(f"L'activité avec ID {id_activite} n'existe pas.")
            return activite
        
        except Exception as e:
            logging.error(f"Erreur lors de la récupération de l'activité : {e}")
            return None

    def lister_activites(self, id_utilisateur: int) -> List[Activite]:
        """Liste toutes les activités d'un utilisateur donné"""
        try:
            # Recherche des activités par utilisateur
            activites = ActiviteDao().lister_par_utilisateur(id_utilisateur=id_utilisateur)

            # Vérification si aucune activité n'est trouvée
            if not activites:
                logging.warning(f"Aucune activité trouvée pour l'utilisateur avec ID {id_utilisateur}.")

            return activites  # Retourne la liste des activités (peut être vide)
    
        except Exception as e:
            # Gestion des exceptions : affichage du message d'erreur
            logging.error(f"Erreur lors de la récupération des activités pour l'utilisateur {id_utilisateur}: {e}")
            return None

    def lister_activites_filtres(self, id_utilisateur: int, sport: str = None, date_debut: str = None, date_fin: str = None) -> List[Activite]:
        """Liste les activités d'un utilisateur avec des filtres optionnels (sport, date_debut, date_fin)"""
        try:
            # Recherche des activités filtrées
            activites = ActiviteDao().lister_activites_filtres(id_utilisateur=id_utilisateur, sport=sport, date_debut=date_debut, date_fin=date_fin)

            # Vérification si aucune activité filtrée n'est trouvée
            if not activites:
                logging.warning(f"Aucune activité trouvée pour l'utilisateur avec ID {id_utilisateur} avec les filtres spécifiés.")

            return activites  # Retourne la liste des activités filtrées (peut être vide)

        except Exception as e:
            # Gestion des exceptions : affichage du message d'erreur
            logging.error(f"Erreur lors de la récupération des activités filtrées pour l'utilisateur {id_utilisateur}: {e}")
            return None


    def ajouter_jaime(self, id_activite: int, id_utilisateur: int) -> bool:
        """Ajoute un "j'aime" à une activité"""
        try:
            jaime = Jaime(id_activite=id_activite, id_auteur=id_utilisateur)
            return JaimeDao().creer(jaime)  # Ajoute le "j'aime" de l'utilisateur
        except Exception as e:
            logging.error(f"Erreur lors de l'ajout du 'j'aime' : {e}")
            return False

    def supprimer_jaime(self, id_activite: int, id_utilisateur: int) -> bool:
        """Supprime un "j'aime" d'une activité"""
        try:
            return JaimeDao().supprimer(id_activite, id_utilisateur)  # Retire le "j'aime" de l'utilisateur
        except Exception as e:
            logging.error(f"Erreur lors de la suppression du 'j'aime' : {e}")
            return False
    
    def compter_jaimes_par_activite(self, id_activite: int) -> int:
        """Compte le nombre de jaimes pour une activité donnée."""
        try:
            nombre = JaimeDao().compter_par_activite(id_activite)
            return nombre
        except Exception as e:
            logging.error(f"Erreur lors du comptage des jaimes d'une activité : {e}")
            return None

    def ajouter_commentaire(self, id_utilisateur: int, id_activite: int, contenu: str) -> bool:
        """Ajoute un commentaire à une activité"""
        try:
            activite = ActiviteDao().trouver_par_id(id_activite=id_activite)
            utilisateur = UtilisateurDao().trouver_par_id(id_utilisateur=id_utilisateur)
            nouveau_commentaire = Commentaire(
                id_activite=id_activite,
                id_auteur=id_utilisateur,
                contenu=contenu,
                date_commentaire=datetime.now()
            )
            return CommentaireDao().creer(nouveau_commentaire)
        except Exception as e:
            logging.error(f"Erreur lors de l'ajout du commentaire : {e}")
            return False

    def supprimer_commentaire(self, id_commentaire: int) -> bool:
        """Supprime un commentaire d'une activité"""
        try:
            # Récupérer le commentaire par son ID
            commentaire = CommentaireDao().trouver_par_id(id_commentaire=id_commentaire)

            # Si le commentaire n'existe pas
            if commentaire is None:
                logging.warning(f"Le commentaire avec ID {id_commentaire} n'existe pas.")
                return False

            # Supprimer le commentaire de la base de données
            return CommentaireDao().supprimer(commentaire)

        except Exception as e:
            logging.error(f"Erreur lors de la suppression du commentaire : {e}")
            return False

    def lister_commentaires(self, id_activite: int) -> List[Commentaire]:
        """Liste tous les commentaires d'une activité"""
        try:
             commentaires = CommentaireDao().lister_par_activite(id_activite=id_activite)  # Méthode dans le DAO
             return commentaires
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des commentaires : {e}")
            return None
    
    def trouver_commentaire_par_id(self, id_commentaire: int) -> Commentaire:
        """Trouver un commentaire par son id"""
        try:
            commentaire = CommentaireDao().trouver_par_id(id_commentaire=id_commentaire)
            # Si le commentaire n'existe pas
            if commentaire is None:
                logging.warning(f"Le commentaire avec ID {id_commentaire} n'existe pas.")
            return commentaire
        
        except Exception as e:
            logging.error(f"Erreur lors de la récupération du commentaire : {e}")
            return None

    def jaime_existe(self, id_activite: int, id_auteur: int) -> bool:
        """Vérifie si un jaime existe dans la base de données"""
        try:
             return JaimeDao().existe(id_activite, id_auteur)
        except Exception as e:
            logging.error(f"Erreur lors de la vérification du jaime : {e}")
            return None

    def abonnement_existe(self, id_utilisateur_suiveur: int, id_utilisateur_suivi: int) -> bool:
        """Vérifie si un abonnement existe dans la base de données"""
        try:
            abonnement = AbonnementDao().trouver_par_ids(id_utilisateur_suiveur, id_utilisateur_suivi)
            return abonnement is not None
        except Exception as e:
            logging.error(f"Erreur lors de la vérification de l'abonnement : {e}")
            return None
