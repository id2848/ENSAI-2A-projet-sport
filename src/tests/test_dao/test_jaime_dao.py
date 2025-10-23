import os
import pytest

from unittest.mock import patch

from utils.reset_database import ResetDatabase

from dao.jaime_dao import JaimeDao

from business_object.jaime import Jaime

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialisation des données de test"""
    with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
        ResetDatabase().lancer(test_dao=True)
        yield

"""
def test_creer_ok():
    # Création d'un jaime réussie

    # GIVEN
    jaime = Jaime(id_activite=991, id_auteur=995)

    # WHEN
    creation_ok = JaimeDao().creer(jaime)

    # THEN
    assert creation_ok
    assert jaime.id_activite == 991
    assert jaime.id_auteur == 995


def test_creer_ko():
    # Création d'un jaime échouée (valeurs incorrectes)

    # GIVEN
    jaime = Jaime(id_activite=None, id_auteur=None)

    # WHEN
    creation_ok = JaimeDao().creer(jaime)

    # THEN
    assert not creation_ok

def test_lister_par_activite():
    # Lister tous les jaimes d'une activité

    # GIVEN
    id_activite = 991

    # WHEN
    jaimes = JaimeDao().lister_par_activite(id_activite)
    jaimes_expected = [Jaime(id_activite=991, id_auteur=995)]

    # THEN
    assert isinstance(jaimes, list)
    for j in jaimes:
        assert isinstance(j, Jaime)
    assert jaimes == jaimes_expected

def test_supprimer_ok():
    # Suppression d'un jaime réussie

    # GIVEN
    jaime = Jaime(id_activite=991, id_auteur=993)
    JaimeDao().creer(jaime)

    # WHEN
    suppression_ok = JaimeDao().supprimer(jaime)

    # THEN
    assert suppression_ok


def test_supprimer_ko():
    # Suppression d'un jaime échouée (id inconnu)

    # GIVEN
    jaime = Jaime(id_activite=9999, id_auteur=9999)  # Jaime inexistant

    # WHEN
    suppression_ok = JaimeDao().supprimer(jaime)

    # THEN
    assert not suppression_ok
"""

def test_existe_ok():
    """Vérifier qu'un jaime existe pour une activité et un auteur donnés"""

    # GIVEN
    jaime = Jaime(id_activite=991, id_auteur=995)
    JaimeDao().creer(jaime)  # Créer un jaime pour pouvoir le tester

    # WHEN
    existe = JaimeDao().existe(id_activite=991, id_auteur=995)

    # THEN
    assert existe


def test_existe_ko():
    """Vérifier qu'un jaime n'existe pas"""

    # GIVEN
    id_activite = 991
    id_auteur = 994

    # WHEN
    existe = JaimeDao().existe(id_activite=id_activite, id_auteur=id_auteur)

    # THEN
    assert (not existe)