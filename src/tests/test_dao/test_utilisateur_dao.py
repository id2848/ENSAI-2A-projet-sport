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


"""def test_supprimer_ok():
    en attente soucis clé etrangere

    # GIVEN
    utilisateur = Utilisateur(id_utilisateur=995, pseudo="mikebrown",mot_de_passe_hash="hash5", nom="Brown", prenom="Mike", date_de_naissance="1988-11-30", sexe="Homme")

    # WHEN
    suppression_ok = UtilisateurDao().supprimer(utilisateur)

    # THEN
    assert suppression_ok
"""

def test_supprimer_ko():
    """Suppression d'utilisateur échouée (id inconnu)"""

    # GIVEN
    utilisateur = Utilisateur(id_utilisateur=8888, pseudo="id inconnu",mot_de_passe_hash="inconnu",nom="nada", prenom="yapa", date_de_naissance="1988-11-30", sexe="Homme")

    # WHEN
    suppression_ok = UtilisateurDao().supprimer(utilisateur)

    # THEN
    assert not suppression_ok


"""def test_se_connecter_ok():
en attente.. soucis hash_password
    # GIVEN
    pseudo = "johndo"
    mdp = "hash1"


    # WHEN
    utilisateur = UtilisateurDao().se_connecter(pseudo, hash_password(mdp, pseudo))

    # THEN
    assert isinstance(utilisateur, Utilisateur)

 """
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
