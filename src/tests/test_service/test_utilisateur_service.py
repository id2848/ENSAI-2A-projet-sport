import pytest
from datetime import date, timedelta
from service.utilisateur_service import UtilisateurService
from dao.utilisateur_dao import UtilisateurDao
from business_object.utilisateur import Utilisateur

import os
import bcrypt
from unittest.mock import patch
from utils.reset_database import ResetDatabase

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Initialisation des données de test dans la base de données"""
    # Assurez-vous d'utiliser un schéma de test pour éviter de modifier la vraie base de données
    with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
        # Reset de la base de données avant de commencer
        ResetDatabase().lancer(test_dao=True)
        yield


# Test de l'inscription avec des données valides
def test_inscrire_valide():
    """Test de l'inscription d'un utilisateur avec des données valides"""

    # GIVEN
    service = UtilisateurService()

    # WHEN
    utilisateur = service.inscrire(
        pseudo="quices123",
        mot_de_passe="monMDP!",
        nom="Qui",
        prenom="Ces",
        date_de_naissance="1990-01-01",
        sexe="masculin"
    )

    # THEN
    assert utilisateur is not None
    assert utilisateur.pseudo == "quices123"


# Test de l'inscription avec un pseudo trop court
def test_inscrire_pseudo_trop_court():
    """Test de l'inscription avec un pseudo trop court"""

    # GIVEN
    service = UtilisateurService()

    # WHEN
    utilisateur = service.inscrire(
        pseudo="qc",  # Pseudo trop court
        mot_de_passe="monMotDePasse!",
        nom="Qui",
        prenom="Ces",
        date_de_naissance="1990-01-01",
        sexe="masculin"
    )

    # THEN
    assert utilisateur is None  # L'inscription doit échouer


# Test de l'inscription avec un mot de passe trop court
def test_inscrire_mot_de_passe_trop_court():
    """Test de l'inscription avec un mot de passe trop court"""

    # GIVEN
    service = UtilisateurService()

    # WHEN
    utilisateur = service.inscrire(
        pseudo="quices123",
        mot_de_passe="123",  # Mot de passe trop court
        nom="Qui",
        prenom="Ces",
        date_de_naissance="1990-01-01",
        sexe="masculin"
    )

    # THEN
    assert utilisateur is None  # L'inscription doit échouer


# Test de l'inscription avec un nom invalide (contenant des chiffres)
def test_inscrire_nom_invalide():
    """Test de l'inscription avec un nom invalide"""

    # GIVEN
    service = UtilisateurService()

    # WHEN
    utilisateur = service.inscrire(
        pseudo="quices123",
        mot_de_passe="monMotDePasse!",
        nom="Qui123",  # Nom invalide
        prenom="Ces",
        date_de_naissance="1990-01-01",
        sexe="masculin"
    )

    # THEN
    assert utilisateur is None  # L'inscription doit échouer


# Test de l'inscription avec une date de naissance invalide
def test_inscrire_date_naissance_invalide():
    """Test de l'inscription avec une date de naissance invalide"""

    # GIVEN
    service = UtilisateurService()

    # WHEN
    utilisateur = service.inscrire(
        pseudo="quices123",
        mot_de_passe="monMotDePasse!",
        nom="Qui",
        prenom="Ces",
        date_de_naissance="01-01-1990",  # Mauvais format de date
        sexe="masculin"
    )

    # THEN
    assert utilisateur is None  # L'inscription doit échouer


# Test de l'inscription avec un sexe invalide
def test_inscrire_sexe_invalide():
    """Test de l'inscription avec un sexe invalide"""

    # GIVEN
    service = UtilisateurService()

    # WHEN
    utilisateur = service.inscrire(
        pseudo="quices123",
        mot_de_passe="monMotDePasse!",
        nom="Qui",
        prenom="Ces",
        date_de_naissance="1990-01-01",
        sexe="alien"  # Sexe invalide
    )

    # THEN
    assert utilisateur is None  # L'inscription doit échouer


# Test de la connexion avec un pseudo correct et mot de passe correct
def test_se_connecter_valide():
    """Test de la connexion avec des données valides"""

    # GIVEN
    service = UtilisateurService()

    # WHEN
    utilisateur = service.se_connecter("quices123", "monMotDePasse!")

    # THEN
    assert utilisateur is not None
    assert utilisateur.pseudo == "quices123"


# Test de la connexion avec un pseudo incorrect
def test_se_connecter_pseudo_incorrect():
    """Test de la connexion avec un pseudo incorrect"""

    # GIVEN
    service = UtilisateurService()

    # WHEN
    utilisateur = service.se_connecter("pseudo_incorrect", "monMotDePasse!")

    # THEN
    assert utilisateur is None

def test_lister_utilisateurs():
    """Test pour lister tous les utilisateurs"""

    # GIVEN
    # WHEN
    liste = UtilisateurService().lister_utilisateurs()

    # THEN
    assert len(liste) > 1


def test_trouver_par_id_ok():
    """Recherche par id d'un utilisateur existant"""

    # GIVEN
    id = 995

    # WHEN
    utilisateur = UtilisateurService().trouver_par_id(id)

    # THEN
    assert utilisateur is not None

def test_trouver_par_id_ko():
    """Recherche par id d'un utilisateur n'existant pas"""

    # GIVEN
    id = 606

    # WHEN
    utilisateur = UtilisateurService().trouver_par_id(id)

    # THEN
    assert utilisateur is None

def test_trouver_par_pseudo_ok():
    """Recherche par pseudo d'un utilisateur existant"""

    # GIVEN
    pseudo = 'mikebrown'

    # WHEN
    utilisateur = UtilisateurService().trouver_par_pseudo(pseudo)

    # THEN
    assert utilisateur is not None

def test_trouver_par_pseudo_ko():
    """Recherche par pseudo d'un utilisateur existant"""

    # GIVEN
    pseudo = 'pppppp'

    # WHEN
    utilisateur = UtilisateurService().trouver_par_pseudo(pseudo)

    # THEN
    assert utilisateur is None

if __name__ == "__main__":
    import pytest
    pytest.main([__file__])

