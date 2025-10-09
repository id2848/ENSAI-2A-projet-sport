import os
import pytest

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
    utilisateur = Utilisateur(pseudo="gg", nom="titi",prenom="tata")

    # WHEN
    creation_ok = UtilisateurDao().creer(utilisateur)

    # THEN
    assert creation_ok
    assert joueur.id_utilisateur


def test_creer_ko():
    """Création d'utilisateur échouée (nom et date de naissance)"""

    # GIVEN
    joueur = Joueur(pseudo="gg", date_de_naissance="chaine de caractere", nom=12)

    # WHEN
    creation_ok = UtilisateurDao().creer(utilisateur)

    # THEN
    assert not creation_ok


def test_modifier_ok():
    """Modification d'utilisateur réussie"""

    # GIVEN
    new_nom = "Black"
    utilisateur = Utilisateur(id_joueur=995, pseudo="mikebrown", nom=new_nom)

    # WHEN
    modification_ok = UtilisteurDao().modifier(utilisateur)

    # THEN
    assert modification_ok


def test_modifier_ko():
    """Modification d'utilisateur' échouée (id inconnu)"""

    # GIVEN
    utilisateur = Utilisateur(id_utilisateur=8888, pseudo="id inconnu", nom="neant")

    # WHEN
    modification_ok = UtilisateurDao().modifier(utilisateur)

    # THEN
    assert not modification_ok


def test_supprimer_ok():
    """Suppression d'utilisateur réussie"""

    # GIVEN
    utilisateur = Utilsateur(id_joueur=995, pseudo="mikebrown")

    # WHEN
    suppression_ok = UtilisateurDao().supprimer(utilisateur)

    # THEN
    assert suppression_ok


def test_supprimer_ko():
    """Suppression d'utilisateur échouée (id inconnu)"""

    # GIVEN
    utilisateur = Utilisateur(id_utilisateur=8888, pseudo="id inconnu",nom="nada")

    # WHEN
    suppression_ok = UtilisateurDao().supprimer(utilisateur)

    # THEN
    assert not suppression_ok


def test_se_connecter_ok():
    """Connexion d'utilisateur réussie"""

    # GIVEN
    pseudo = "johndo"
    mdp = "hash1"

    # WHEN
    utilisateur = UtilisateurDao().se_connecter(pseudo, hash_password(mdp, pseudo))

    # THEN
    assert isinstance(utilisateurr, Utilisateur)


def test_se_connecter_ko():
    """Connexion d'utilisateur échouée (pseudo ou mdp incorrect)"""

    # GIVEN
    pseudo = "toto"
    mdp = "poiuytreza"

    # WHEN
    utilisateur = UtilisateurDao().se_connecter(pseudo, hash_password(mdp, pseudo))

    # THEN
    assert not utilisateur


if __name__ == "__main__":
    pytest.main([__file__])
