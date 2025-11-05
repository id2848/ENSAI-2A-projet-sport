import os
import pytest
from datetime import timedelta, date
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


def test_calculer_nombre_activites_ok():
    """Nombre d'activités correct pour un utilisateur existant"""

    # GIVEN
    id_utilisateur = 991  

    # WHEN
    activites = ActiviteDao().lister_par_utilisateur(id_utilisateur)
    nombre = len(activites)

    # THEN
    assert nombre > 0


def test_calculer_nombre_activites_ko():
    """Nombre d'activités pour un utilisateur sans activité"""

    # GIVEN
    id_utilisateur = 9999  # utilisateur sans activité

    # WHEN
    activites = ActiviteDao().lister_par_utilisateur(id_utilisateur)
    nombre = len(activites)

    # THEN
    assert nombre == 0


def test_calculer_distance_totale_ok():
    """Distance totale correcte pour un utilisateur existant"""

    # GIVEN
    id_utilisateur = 991  # utilisateur existant

    # WHEN
    activites = ActiviteDao().lister_par_utilisateur(id_utilisateur)
    distance_totale = sum(a.distance for a in activites)

    # THEN
    assert distance_totale > 0


def test_calculer_distance_totale_ko():
    """Distance totale pour un utilisateur sans activité"""

    # GIVEN
    id_utilisateur = 9999  # utilisateur sans activité

    # WHEN
    activites = ActiviteDao().lister_par_utilisateur(id_utilisateur)
    distance_totale = sum(a.distance for a in activites)

    # THEN
    assert distance_totale == 0.0


def test_calculer_duree_totale_ok():
    """Durée totale correcte pour un utilisateur existant"""

    # GIVEN
    id_utilisateur = 991  # utilisateur existant
    dao = ActiviteDao()

    # WHEN
    activites = ActiviteDao().lister_par_utilisateur(id_utilisateur)
    duree_totale = int(sum(a.duree if isinstance(a.duree, (int, float)) else a.duree.total_seconds()
    for a in activites))

    # THEN
    assert duree_totale > 0


def test_calculer_duree_totale_ko():
    """Durée totale pour un utilisateur sans activité"""

    # GIVEN
    id_utilisateur = 9999  # utilisateur sans activité

    # WHEN
    activites = ActiviteDao().lister_par_utilisateur(id_utilisateur)
    duree_totale = int(sum(a.duree.total_seconds() for a in activites))

    # THEN
    assert duree_totale == 0
