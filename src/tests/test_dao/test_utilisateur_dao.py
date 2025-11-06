import os
import pytest
import bcrypt

from unittest.mock import patch

from utils.reset_database import ResetDatabase
from utils.securite import hash_password

from dao.utilisateur_dao import UtilisateurDao

from business_object.utilisateur import Utilisateur


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialisation des données de test"""
    with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
        ResetDatabase().lancer(test_dao=True)
        yield


def test_trouver_par_id_existant():
    """Recherche par id d'un utilisateur existant"""

    # GIVEN
    id_utilisateur = 992

    # WHEN
    utilisateur = UtilisateurDao().trouver_par_id(id_utilisateur)

    # THEN
    assert utilisateur is not None


def test_trouver_par_id_non_existant():
    """Recherche par id d'un utilisateur n'existant pas"""

    # GIVEN
    id_utilisateur = 9999999999999

    # WHEN
    utilisateur = UtilisateurDao().trouver_par_id(id_utilisateur)

    # THEN
    assert utilisateur is None


def test_trouver_par_pseudo_ok():
    """Recherche par pseudo d'un utilisateur existant"""

    # GIVEN
    pseudo = 'samsmith'

    # WHEN
    utilisateur = UtilisateurDao().trouver_par_pseudo(pseudo)

    # THEN
    assert utilisateur is not None


def test_trouver_par_pseudo_ko():
    """Recherche par pseudo d'un utilisateur n'existant pas"""

    # GIVEN
    pseudo = 'iiiiii'

    # WHEN
    utilisateur = UtilisateurDao().trouver_par_pseudo(pseudo)

    # THEN
    assert utilisateur is None




def test_lister_tous():
    """Vérifie que la méthode renvoie une liste d'utilisateur
    de taille supérieure ou égale à 2
    """

    # GIVEN

    # WHEN
    utilisateurs = UtilisateurDao().lister_tous()

    # THEN
    assert isinstance(utilisateurs, list)
    for j in utilisateurs:
        assert isinstance(j, Utilisateur)
    assert len(utilisateurs) >= 2



def test_creer_ok():
    """Création d'utilisateur réussie"""

    # GIVEN
    utilisateur = Utilisateur(pseudo="gg", nom="titi",prenom="tata",mot_de_passe_hash="hash1",date_de_naissance="1990-01-02",sexe="Homme")

    # WHEN
    creation_ok = UtilisateurDao().creer(utilisateur)

    # THEN
    assert creation_ok
    assert utilisateur.id_utilisateur


def test_creer_ko():
    """Création d'utilisateur échouée (nom et date de naissance)"""

    # GIVEN
    utilisateur = Utilisateur(pseudo="gg", date_de_naissance="chaine de caractere", nom=12,mot_de_passe_hash="hash1",prenom=13,sexe="Homme")

    # WHEN
    creation_ok = UtilisateurDao().creer(utilisateur)

    # THEN
    assert not creation_ok


def test_modifier_ok():
    """Modification d'utilisateur réussie"""

    # GIVEN
    new_nom = "Black"
    new_prenom = "white"
    new_date="2020-11-30"
    new_sexe="Femme"
    utilisateur = Utilisateur(id_utilisateur=995, pseudo="mikebrown", mot_de_passe_hash="hash5", nom=new_nom, prenom=new_prenom, date_de_naissance=new_date, sexe=new_sexe)

    # WHEN
    modification_ok = UtilisateurDao().modifier(utilisateur)

    # THEN
    assert modification_ok


def test_modifier_ko():
    """Modification d'utilisateur' échouée (id inconnu)"""

    # GIVEN
    utilisateur = Utilisateur(id_utilisateur=8888, pseudo="id inconnu", mot_de_passe_hash="nada", nom="neant",prenom="rien",date_de_naissance="2020-01-01",sexe="Homme")

    # WHEN
    modification_ok = UtilisateurDao().modifier(utilisateur)

    # THEN
    assert not modification_ok


def test_supprimer_ok():
    """Suppression d'utilisateurréussie (sans problème de clé étrangère)"""

    # GIVEN
    utilisateur = Utilisateur(id_utilisateur=995, pseudo="unique_mikebrown",mot_de_passe_hash="hash5", nom="Brown", prenom="Mike", date_de_naissance="1988-11-30", sexe="Homme")
    # Création de l'utilisateur dans la base de données
    creation_ok = UtilisateurDao().creer(utilisateur)
    assert creation_ok, "La création de l'utilisateur a échoué"
    
    # Vérification que l'utilisateur a bien été créé
    utilisateur_cree = UtilisateurDao().trouver_par_id(utilisateur.id_utilisateur)
    assert utilisateur_cree is not None, "L'utilisateur créé n'est pas trouvé dans la base de données"

    # WHEN
    suppression_ok = UtilisateurDao().supprimer(utilisateur)

    # THEN
    assert suppression_ok,"La suppression de l'utilisateur a échoué"
    # Vérification supplémentaire : après suppression, l'utilisateur ne doit plus exister dans la base de données
    utilisateur_supprime = UtilisateurDao().trouver_par_id(utilisateur.id_utilisateur)
    assert utilisateur_supprime is None, "L'utilisateur n'a pas été correctement supprimé de la base de données"



def test_supprimer_ko():
    """Suppression d'utilisateur échouée (id inconnu)"""

    # GIVEN
    utilisateur = Utilisateur(id_utilisateur=8888, pseudo="id inconnu",mot_de_passe_hash="inconnu",nom="nada", prenom="yapa", date_de_naissance="1988-11-30", sexe="Homme")

    # WHEN
    suppression_ok = UtilisateurDao().supprimer(utilisateur)

    # THEN
    assert not suppression_ok

    

def test_verifier_pseudo_existant():
    """Vérifier que la méthode retourne True si le pseudo existe déjà"""
    # GIVEN
    utilisateur_dao = UtilisateurDao()
    pseudo_existant = "samsmith"  # Exemple d'un pseudo existant dans la base de données
    
    # WHEN
    existe = utilisateur_dao.verifier_pseudo_existant(pseudo_existant)
    
    # THEN
    assert existe is True  # Le pseudo existe dans la base de données

def test_verifier_pseudo_non_existant():
    """Vérifier que la méthode retourne False si le pseudo n'existe pas"""
    # GIVEN
    utilisateur_dao = UtilisateurDao()
    pseudo_non_existant = "nouveau_pseudo"  # Un pseudo qui n'existe pas dans la base de données
    
    # WHEN
    existe = utilisateur_dao.verifier_pseudo_existant(pseudo_non_existant)
    
    # THEN
    assert existe is False  # Le pseudo n'existe pas dans la base de données
def test_se_connecter_ok():
    """Test de la connexion avec un pseudo et un mot de passe correct"""
    
    # GIVEN
    pseudo = "johndo"
    mdp = "hash1"
    # Création de l'utilisateur avec le mot de passe haché
    utilisateur = Utilisateur(pseudo=pseudo, mot_de_passe_hash=hash_password(mdp, pseudo), nom="Doe", prenom="John", date_de_naissance="1990-01-01", sexe="Homme")
    creation_ok = UtilisateurDao().creer(utilisateur)
    
    assert creation_ok, "La création de l'utilisateur a échoué"
    
    # WHEN: Tentative de connexion avec le pseudo et le mot de passe
    utilisateur_connecte = UtilisateurDao().se_connecter(pseudo, hash_password(mdp, pseudo))
    
    # THEN: La connexion doit réussir, donc l'utilisateur retourné doit être une instance de Utilisateur
    assert isinstance(utilisateur_connecte, Utilisateur), "La connexion a échoué, l'utilisateur retourné n'est pas valide"

def test_se_connecter_ko():
    """Test de la connexion échouée avec pseudo ou mot de passe incorrect"""
    
    # GIVEN: Création préalable d'un utilisateur avec un pseudo et un mot de passe
    pseudo = "johndo"
    mdp = "hash1"  # Le mot de passe correct
    
    utilisateur = Utilisateur(pseudo=pseudo, mot_de_passe_hash=hash_password(mdp, pseudo), nom="Doe", prenom="John", date_de_naissance="1990-01-01", sexe="Homme")
    creation_ok = UtilisateurDao().creer(utilisateur)
    assert creation_ok, "La création de l'utilisateur a échoué"
    
    # WHEN: Tentative de connexion avec un mot de passe incorrect
    mauvais_mdp = "wrong_password"
    utilisateur_connecte = UtilisateurDao().se_connecter(pseudo, hash_password(mauvais_mdp, pseudo))
    
    # THEN: La connexion doit échouer, donc l'utilisateur retourné doit être None
    assert utilisateur_connecte is None, "La connexion a échoué, mais l'utilisateur a été trouvé avec un mot de passe incorrect"
    
def test_creer_ok():
    """Création d'utilisateur réussie"""
    
    # GIVEN
    utilisateur = Utilisateur(pseudo="gg", nom="titi", prenom="tata", mot_de_passe_hash="hash1", date_de_naissance="1990-01-02", sexe="Homme")
    
    # WHEN
    creation_ok = UtilisateurDao().creer(utilisateur)
    
    # THEN
    assert creation_ok
    assert utilisateur.id_utilisateur is not None  # L'ID de l'utilisateur doit être défini après la création

