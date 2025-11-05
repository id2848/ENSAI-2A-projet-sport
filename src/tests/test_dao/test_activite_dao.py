import os
import pytest
from unittest.mock import patch

from utils.reset_database import ResetDatabase
from dao.activite_dao import ActiviteDao
from business_object.activite import Activite

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialisation des données de test dans le schéma dédié aux tests"""
    with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
        ResetDatabase().lancer(test_dao=True)
        yield


def test_creer_ko_utilisateur_inexistant():
    """Création d'une activité échouée (id_utilisateur inexistant)"""
    # GIVEN
    activite = Activite(
        id_activite=3001,
        id_utilisateur=99999,  # utilisateur inexistant
        sport="Natation",
        date_activite="2025-01-01",
        distance=1.2,
        duree=30
    )

    # WHEN
    creation_ok = ActiviteDao().creer(activite)

    # THEN
    assert not creation_ok


def test_creer_ok_utilisateur_existant():
    """Création d'une activité réussie pour un utilisateur existant"""
    # GIVEN
    activite = Activite(
        id_activite=3002,
        id_utilisateur=991,  
        sport="natation",
        date_activite="2025-01-02",
        distance=5.0,
        duree=1800
    )

    # WHEN
    creation_ok = ActiviteDao().creer(activite)

    # THEN
    assert creation_ok


def test_lister_par_utilisateur_ok():
    """Lister les activités d’un utilisateur existant"""
    # GIVEN
    id_utilisateur = 991

    # WHEN
    activites = ActiviteDao().lister_par_utilisateur(id_utilisateur)

    # THEN
    assert isinstance(activites, list)
    for a in activites:
        assert isinstance(a, Activite)
        assert a.id_utilisateur == id_utilisateur


def test_lister_par_utilisateur_vide():
    """Lister les activités d’un utilisateur sans activité"""
    # GIVEN
    id_utilisateur = 9999

    # WHEN
    activites = ActiviteDao().lister_par_utilisateur(id_utilisateur)

    # THEN
    assert isinstance(activites, list)
    assert len(activites) == 0


def test_trouver_par_id_ko():
    """Trouver une activité inexistante via l'id_activite"""
    # GIVEN
    id_activite = 99999

    # WHEN
    activite = ActiviteDao().trouver_par_id(id_activite)

    # THEN
    assert activite is None


def test_trouver_par_id_ok():
    """Trouver une activité existante par son id"""
    # GIVEN
    id_activite = 3002

    # WHEN
    activite = ActiviteDao().trouver_par_id(id_activite)

    # THEN
    assert activite is not None
    assert activite.id_activite == id_activite


def test_modifier_ok():
    """Modification d'une activité existante réussie"""
    # GIVEN
    activite = Activite(
        id_activite=3002,
        id_utilisateur=991,
        sport="randonnée",
        date_activite="2025-01-03",
        distance=6.0,
        duree=2000
    )

    # WHEN
    modification_ok = ActiviteDao().modifier(activite)

    # THEN
    assert modification_ok


def test_modifier_ko():
    """Modification échouée pour une activité inexistante"""
    # GIVEN
    activite = Activite(
        id_activite=99999,
        id_utilisateur=991,
        sport="Marche",
        date_activite="2025-01-03",
        distance=6.0,
        duree=2000
    )

    # WHEN
    modification_ok = ActiviteDao().modifier(activite)

    # THEN
    assert not modification_ok


def test_supprimer_ok():
    """Suppression d'une activité existante réussie"""
    # GIVEN
    activite = Activite(
        id_activite=3002,
        id_utilisateur=991,
        sport="randonnée",
        date_activite="2025-01-03",
        distance=6.0,
        duree=2000
    )

    # WHEN
    suppression_ok = ActiviteDao().supprimer(activite)

    # THEN
    assert suppression_ok


def test_supprimer_ko():
    """Suppression échouée pour une activité inexistante"""
    # GIVEN
    activite = Activite(
        id_activite=99999,
        id_utilisateur=991,
        sport="natation",
        date_activite="2025-01-03",
        distance=3.0,
        duree=1000
    )

    # WHEN
    suppression_ok = ActiviteDao().supprimer(activite)

    # THEN
    assert not suppression_ok
