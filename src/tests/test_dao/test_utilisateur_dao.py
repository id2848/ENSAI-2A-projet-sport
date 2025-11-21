import os
import pytest

from unittest.mock import patch

from utils.reset_database import ResetDatabase
from utils.securite import hash_password

from dao.utilisateur_dao import UtilisateurDao

from business_object.utilisateur import Utilisateur


@pytest.fixture(autouse=True)
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
    assert utilisateur.id_utilisateur == 992
    assert utilisateur.pseudo == "janedoe"


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


def test_modifier_ok():
    """Modification d'utilisateur réussie"""

    # GIVEN
    new_nom = "Black"
    new_prenom = "White"
    new_date="2010-01-01"
    new_sexe="Femme"
    utilisateur = Utilisateur(id_utilisateur=995, pseudo="mikebrown", nom=new_nom, prenom=new_prenom, date_de_naissance=new_date, sexe=new_sexe)

    # WHEN
    modification_ok = UtilisateurDao().modifier(utilisateur)

    # THEN
    assert modification_ok


def test_modifier_ko():
    """Modification d'utilisateur' échouée (id inconnu)"""

    # GIVEN
    utilisateur = Utilisateur(id_utilisateur=8888, pseudo="id inconnu", nom="neant",prenom="rien",date_de_naissance="2020-01-01",sexe="Homme")

    # WHEN
    modification_ok = UtilisateurDao().modifier(utilisateur)

    # THEN
    assert not modification_ok


def test_supprimer_ok():
    """Suppression d'utilisateur réussie"""

    # GIVEN
    id_utilisateur = 995 # existant dans les données test

    # WHEN
    suppression_ok = UtilisateurDao().supprimer(id_utilisateur)

    # THEN
    assert suppression_ok, "La suppression de l'utilisateur a échoué"

    # Vérification supplémentaire : après suppression, l'utilisateur ne doit plus exister dans la base de données
    utilisateur_supprime = UtilisateurDao().trouver_par_id(id_utilisateur)
    assert utilisateur_supprime is None, "L'utilisateur n'a pas été correctement supprimé de la base de données"


def test_supprimer_ko():
    """Suppression d'utilisateur échouée (id inconnu)"""

    # GIVEN
    id_utilisateur = 8888

    # WHEN
    suppression_ok = UtilisateurDao().supprimer(id_utilisateur)

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


def test_creer_ok():
    """Création valide d'un utilisateur"""

    # GIVEN
    u = Utilisateur(
        pseudo="nouveau",
        nom="Dup",
        prenom="Dup",
        date_de_naissance="2000-01-01",
        sexe="Homme"
    )
    mot_de_passe = "supermdp"

    # WHEN
    res = UtilisateurDao().creer(u, mot_de_passe)

    # THEN
    assert res is True
    assert u.id_utilisateur is not None

    # Vérification que l'utilisateur existe réellement
    trouve = UtilisateurDao().trouver_par_id(u.id_utilisateur)
    assert trouve is not None
    assert trouve.pseudo == "nouveau"


def test_creer_ko():
    """Création refusée : pseudo déjà existant"""

    # GIVEN
    u = Utilisateur(
        pseudo="johndoe",     # déjà dans pop_db_test.sql
        nom="Dup",
        prenom="Dup",
        date_de_naissance="2000-01-01",
        sexe="Homme"
    )
    mot_de_passe = "1234"

    # WHEN
    res = UtilisateurDao().creer(u, mot_de_passe)

    # THEN
    assert res is False
    assert u.id_utilisateur is None


def test_se_connecter_ko():
    """Échec connexion avec mauvais mot de passe"""

    # GIVEN
    pseudo = "janedoe"
    mauvais_mdp = "mauvais_mdp"

    # WHEN
    utilisateur = UtilisateurDao().se_connecter(pseudo, mauvais_mdp)

    # THEN
    assert utilisateur is None


def test_se_connecter_ok():
    """
    Connexion OK
    (rappel : mdp dans pop_db_test.sql sont 'mdp1' etc.
    avant que reset_database ne les hache)
    """

    # GIVEN
    pseudo = "janedoe"
    bon_mdp = "mdp2"   # avant le hashing + salt effectué au reset

    # WHEN
    utilisateur = UtilisateurDao().se_connecter(pseudo, bon_mdp)

    # THEN
    assert utilisateur is not None
    assert utilisateur.pseudo == "janedoe"
