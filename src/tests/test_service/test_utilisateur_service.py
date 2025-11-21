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
    res = UtilisateurService().inscrire(pseudo, mot_de_passe, nom, prenom, date_de_naissance, sexe)

    # THEN
    assert res is True  # Le résultat doit être True si l'inscription réussit


def test_inscrire_utilisateur_pseudo_deja_utilise():
    """Test pour l'inscription d'un utilisateur avec un pseudo déjà existant"""

    # GIVEN
    pseudo = "johndoe"  # Pseudo déjà existant dans la base de données de test
    mot_de_passe = "password"
    nom = "Doe"
    prenom = "John"
    date_de_naissance = "1990-01-01"
    sexe = "homme"

    # WHEN / THEN
    with pytest.raises(Exception):
        res = UtilisateurService().inscrire(pseudo, mot_de_passe, nom, prenom, date_de_naissance, sexe)


def test_inscrire_utilisateur_donnees_invalides():
    """Test pour l'inscription avec des données invalides"""

    # GIVEN
    pseudo = "joe°°°"
    mot_de_passe = "123456"
    nom = "Doe"
    prenom = "John"
    date_de_naissance = "1990-01-01"
    sexe = "homme"

    # WHEN / THEN
    with pytest.raises(ValueError):
        res = UtilisateurService().inscrire(pseudo, mot_de_passe, nom, prenom, date_de_naissance, sexe)



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

    # WHEN / THEN
    with pytest.raises(Exception):
        utilisateur = UtilisateurService().se_connecter(pseudo, mot_de_passe)


def test_se_connecter_utilisateur_inexistant():
    """Test pour la connexion d'un utilisateur avec un pseudo inexistant"""

    # GIVEN
    pseudo = "unknownuser"  # Pseudo inexistant
    mot_de_passe = "password"  # Mot de passe correct

    # WHEN / THEN
    with pytest.raises(Exception):
        utilisateur = UtilisateurService().se_connecter(pseudo, mot_de_passe)

if __name__ == "__main__":
    pytest.main([__file__])
    