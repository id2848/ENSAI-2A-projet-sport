import pytest
from datetime import date
from unittest.mock import patch

from service.utilisateur_service import UtilisateurService
from dao.utilisateur_dao import UtilisateurDao
from business_object.utilisateur import Utilisateur

from utils.reset_database import ResetDatabase
import os


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Initialisation des données de test dans la base de données"""
    with patch.dict(os.environ, {"POSTGRES_SCHEMA": "projet_test_dao"}):
        # Reset de la base de données avant de commencer
        ResetDatabase().lancer(test_dao=True)
        yield


# Test de l'inscription
def test_inscrire_utilisateur_ok():
    """Test pour la création d'un utilisateur avec des données valides"""

    # GIVEN
    pseudo = "john123"
    mot_de_passe = "password"
    nom = "Doe"
    prenom = "John"
    date_de_naissance = "1990-01-01"
    sexe = "homme"

    # WHEN
    resultat = UtilisateurService().inscrire(pseudo, mot_de_passe, nom, prenom, date_de_naissance, sexe)

    # THEN
    assert resultat is True  # Le résultat doit être True si l'inscription réussit


def test_inscrire_utilisateur_pseudo_deja_utilise():
    """Test pour l'inscription d'un utilisateur avec un pseudo déjà existant"""

    # GIVEN
    pseudo = "johndoe"  # Pseudo déjà existant dans la base de données de test
    mot_de_passe = "password"
    nom = "Doe"
    prenom = "John"
    date_de_naissance = "1990-01-01"
    sexe = "homme"

    # WHEN
    resultat = UtilisateurService().inscrire(pseudo, mot_de_passe, nom, prenom, date_de_naissance, sexe)

    # THEN
    assert resultat is False  # Le pseudo existe déjà, l'inscription doit échouer


def test_inscrire_utilisateur_donnees_invalides():
    """Test pour l'inscription avec des données invalides"""

    # GIVEN
    pseudo = "jo"
    mot_de_passe = "123"
    nom = "Doe"
    prenom = "John"
    date_de_naissance = "1990-01-01"
    sexe = "homme"

    # WHEN
    resultat = UtilisateurService().inscrire(pseudo, mot_de_passe, nom, prenom, date_de_naissance, sexe)

    # THEN
    assert resultat is False  # Le pseudo et mot de passe sont invalides


# Test de la connexion
def test_se_connecter_utilisateur_ok():
    """Test pour la connexion d'un utilisateur avec des identifiants valides"""

    # GIVEN
    pseudo = "johndoe"  # Pseudo existant
    mot_de_passe = "mdp1"  # Mot de passe correct

    # WHEN
    utilisateur = UtilisateurService().se_connecter(pseudo, mot_de_passe)

    # THEN
    assert utilisateur is not None  # L'utilisateur doit être trouvé
    assert utilisateur.pseudo == pseudo  # L'utilisateur doit avoir le bon pseudo


def test_se_connecter_utilisateur_mot_de_passe_incorrect():
    """Test pour la connexion d'un utilisateur avec un mot de passe incorrect"""

    # GIVEN
    pseudo = "johndoe"  # Pseudo existant
    mot_de_passe = "wrongpassword"  # Mot de passe incorrect

    # WHEN
    utilisateur = UtilisateurService().se_connecter(pseudo, mot_de_passe)

    # THEN
    assert utilisateur is None  # La connexion échoue car le mot de passe est incorrect


def test_se_connecter_utilisateur_inexistant():
    """Test pour la connexion d'un utilisateur avec un pseudo inexistant"""

    # GIVEN
    pseudo = "unknownuser"  # Pseudo inexistant
    mot_de_passe = "password"  # Mot de passe correct

    # WHEN
    utilisateur = UtilisateurService().se_connecter(pseudo, mot_de_passe)

    # THEN
    assert utilisateur is None  # La connexion échoue car l'utilisateur n'existe pas


# Test des validations
def test_valider_pseudo():
    """Test pour la validation du pseudo"""

    # GIVEN
    pseudo_valide = "valid123"
    pseudo_invalide = "in"  # Trop court

    # WHEN
    validation_valide = UtilisateurService().valider_pseudo(pseudo_valide)
    validation_invalide = UtilisateurService().valider_pseudo(pseudo_invalide)

    # THEN
    assert validation_valide is True  # Le pseudo valide doit être accepté
    assert validation_invalide is False  # Le pseudo invalide doit être rejeté


def test_valider_mot_de_passe():
    """Test pour la validation du mot de passe"""

    # GIVEN
    mot_de_passe_valide = "valid123"
    mot_de_passe_invalide = "123"  # Trop court

    # WHEN
    validation_valide = UtilisateurService().valider_mot_de_passe(mot_de_passe_valide)
    validation_invalide = UtilisateurService().valider_mot_de_passe(mot_de_passe_invalide)

    # THEN
    assert validation_valide is True  # Le mot de passe valide doit être accepté
    assert validation_invalide is False  # Le mot de passe invalide doit être rejeté


def test_valider_nom_prenom():
    """Test pour la validation du nom et prénom"""

    # GIVEN
    nom_valide = "Doe"
    prenom_valide = "John"
    nom_invalide = "Doe123"
    prenom_invalide = "John@"

    # WHEN
    validation_valide = UtilisateurService().valider_nom_prenom(nom_valide, prenom_valide)
    validation_invalide = UtilisateurService().valider_nom_prenom(nom_invalide, prenom_invalide)

    # THEN
    assert validation_valide is True  # Nom et prénom valides
    assert validation_invalide is False  # Nom et prénom invalides


def test_valider_date_naissance():
    """Test pour la validation de la date de naissance"""

    # GIVEN
    date_valide = "1990-01-01"
    date_invalide = "01-01-1990"  # Mauvais format

    # WHEN
    validation_valide = UtilisateurService().valider_date_naissance(date_valide)
    validation_invalide = UtilisateurService().valider_date_naissance(date_invalide)

    # THEN
    assert validation_valide is True  # La date doit être valide
    assert validation_invalide is False  # La date doit être invalide


def test_valider_sexe():
    """Test pour la validation du sexe"""

    # GIVEN
    sexe_valide = "homme"
    sexe_invalide = "invalide"  # Sexe non reconnu

    # WHEN
    validation_valide = UtilisateurService().valider_sexe(sexe_valide)
    validation_invalide = UtilisateurService().valider_sexe(sexe_invalide)

    # THEN
    assert validation_valide is True  # Sexe valide
    assert validation_invalide is False  # Sexe invalide
