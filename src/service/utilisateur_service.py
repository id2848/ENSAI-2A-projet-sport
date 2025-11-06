from typing import List
from datetime import date, datetime, timedelta

from utils.log_decorator import log
from utils.securite import hash_password

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
import bcrypt

class UtilisateurService:
    """Classe contenant les méthodes de service d'Utilisateurs"""

 
    @log
    def inscrire(self, pseudo, mot_de_passe, nom, prenom, date_de_naissance, sexe):
        # Vérification de la longueur du mot de passe
        if len(mot_de_passe) < 5 or len(mot_de_passe) > 10:
            logging.error("Le mot de passe doit comporter entre 5 et 10 caractères.")
            return None  # Retourne None si le mot de passe est invalide

        # Hachage du mot de passe avec bcrypt
        salt = bcrypt.gensalt()
        mot_de_passe_hash = bcrypt.hashpw(mot_de_passe.encode(), salt)

        # Création de l'utilisateur avec le mot de passe haché
        utilisateur = Utilisateur(
            pseudo=pseudo,
            mot_de_passe_hash=mot_de_passe_hash,
            nom=nom,
            prenom=prenom,
            date_de_naissance=date_de_naissance,
            sexe=sexe,
        )

        # Tentative de création de l'utilisateur
        if UtilisateurDao().creer(utilisateur):
            return utilisateur
        return None  # Retourne None si la création échoue

    @log
    def se_connecter(self, pseudo, mot_de_passe):
        """Se connecter à un utilisateur"""
        
        utilisateur = UtilisateurDao().se_connecter(pseudo, hash_password(mot_de_passe, pseudo))
        
        if utilisateur:
            return utilisateur
        else:
            logging.error(f"Échec de la connexion pour {pseudo}")
            return None

    def valider_pseudo(self, pseudo: str) -> bool:
        """Valider que le pseudo est valide et unique (entre 5 et 10 caractères)"""
        if len(pseudo) < 5 or len(pseudo) > 10 or not pseudo.isalnum():
            return False
        utilisateur_dao = UtilisateurDao()
        return not utilisateur_dao.verifier_pseudo_existant(pseudo)

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
        """Valider que le sexe est masculin, féminin ou autre"""
        return sexe.lower() in ['masculin', 'féminin', 'autre']


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
            # Gestion des exceptions : affichage du message d'erreur
            print(f"Erreur lors de la récupération des utilisateurs: {e}")
            return []  # Retourne une liste vide en cas d'erreur


    def trouver_par_id(self, id_utilisateur) -> Utilisateur:
        """Trouver un Utilisateur à partir de son id"""
        return UtilisateurDao().trouver_par_id(id_utilisateur)


    def trouver_par_pseudo(self, pseudo) -> Utilisateur:
        """Trouver un Utilisateur à partir de son pseudo"""
        return UtilisateurDao().trouver_par_pseudo(pseudo)