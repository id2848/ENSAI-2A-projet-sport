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

def test_creer_ok():
    """Création d'un jaime réussie"""

    # GIVEN
    jaime = Jaime(id_activite=991, id_auteur=994)

    # WHEN
    creation_ok = JaimeDao().creer(jaime)

    # THEN
    assert creation_ok
    assert jaime.id_activite == 991
    assert jaime.id_auteur == 994

def test_creer_ko_id_activite():
    """Création d'un jaime échouée (id_activite incorrect)"""

    # GIVEN
    jaime = Jaime(id_activite=99999, id_auteur=994)

    # WHEN
    creation_ok = JaimeDao().creer(jaime)

    # THEN
    assert not creation_ok

def test_creer_ko_id_auteur():
    """Création d'un jaime échouée (id_auteur incorrect)"""

    # GIVEN
    jaime = Jaime(id_activite=991, id_auteur=99999)

    # WHEN
    creation_ok = JaimeDao().creer(jaime)

    # THEN
    assert not creation_ok

def test_lister_par_activite():
    """Lister tous les jaimes d'une activité"""

    # GIVEN
    id_activite = 992 # issue données test
    jaimes_expected = [Jaime(id_activite=992, id_auteur=994)]

    # WHEN
    jaimes = JaimeDao().lister_par_activite(id_activite)

    # THEN
    assert isinstance(jaimes, list)
    for j in jaimes:
        assert isinstance(j, Jaime)
    for j, expected in zip(jaimes, jaimes_expected):
        assert j.id_activite == expected.id_activite
        assert j.id_auteur == expected.id_auteur

def test_supprimer_ok():
    """Suppression d'un jaime réussie"""

    # GIVEN
    jaime = Jaime(id_activite=993, id_auteur=991) # issu données test

    # WHEN
    suppression_ok = JaimeDao().supprimer(jaime)

    # THEN
    assert suppression_ok

def test_supprimer_ko_1():
    """Suppression d'un jaime échouée (jaime inexistant)"""

    # GIVEN
    jaime = Jaime(id_activite=991, id_auteur=995)

    # WHEN
    suppression_ok = JaimeDao().supprimer(jaime)

    # THEN
    assert not suppression_ok

def test_supprimer_ko_id_activite():
    """Suppression d'un jaime échouée (id_activite inexistant)"""

    # GIVEN
    jaime = Jaime(id_activite=9999, id_auteur=991)

    # WHEN
    suppression_ok = JaimeDao().supprimer(jaime)

    # THEN
    assert not suppression_ok

def test_supprimer_ko_id_auteur():
    """Suppression d'un jaime échouée (id_auteur inexistant)"""

    # GIVEN
    jaime = Jaime(id_activite=991, id_auteur=9999)

    # WHEN
    suppression_ok = JaimeDao().supprimer(jaime)

    # THEN
    assert not suppression_ok

def test_existe_ok():
    """Vérifier qu'un jaime existe pour une activité et un auteur donnés"""

    # GIVEN
    id_activite=991
    id_auteur=993

    # WHEN
    existe = JaimeDao().existe(id_activite=id_activite, id_auteur=id_auteur)

    # THEN
    assert existe


def test_existe_ko():
    """Vérifier qu'un jaime n'existe pas"""

    # GIVEN
    id_activite = 991
    id_auteur = 995

    # WHEN
    existe = JaimeDao().existe(id_activite=id_activite, id_auteur=id_auteur)

    # THEN
    assert (not existe)