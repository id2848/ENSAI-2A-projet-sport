import os
import pytest
from datetime import date
from unittest.mock import patch

from utils.reset_database import ResetDatabase
from dao.activite_dao import ActiviteDao
from business_object.activite import Activite
from service.service_statistiques import ServiceStatistiques


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialisation des données de test dans le schéma dédié aux tests"""
    with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
        ResetDatabase().lancer(test_dao=True)
        yield

def test_calculer_nombre_activites_totale_ok():
    """Nombre d'activités par sport correct pour un utilisateur existant"""

    # GIVEN
    id_utilisateur = 991
    service = ServiceStatistiques()

    # WHEN
    resultat = service.calculer_nombre_activites_totale(id_utilisateur)

    # THEN
    assert isinstance(resultat, dict)
    if resultat:
        assert all(isinstance(k, str) for k in resultat.keys())
        assert all(isinstance(v, int) for v in resultat.values())
    else:
        pytest.skip("Aucune activité trouvée pour cet utilisateur.")


def test_calculer_nombre_activites_totale_ko():
    """Aucune activité pour un utilisateur inexistant"""

    # GIVEN
    id_utilisateur = 9999
    service = ServiceStatistiques()

    # WHEN
    resultat = service.calculer_nombre_activites_totale(id_utilisateur)

    # THEN
    assert isinstance(resultat, dict)
    assert resultat == {}


def test_calculer_distance_totale_ok():
    """Distance totale correcte pour un utilisateur existant"""

    # GIVEN
    id_utilisateur = 991
    service = ServiceStatistiques()

    # WHEN
    resultat = service.calculer_distance_totale(id_utilisateur)

    # THEN
    assert isinstance(resultat, (int, float))
    assert resultat >= 0.0


def test_calculer_distance_totale_ko():
    """Distance totale pour un utilisateur sans activité"""

    # GIVEN
    id_utilisateur = 9999
    service = ServiceStatistiques()

    # WHEN
    resultat = service.calculer_distance_totale(id_utilisateur)

    # THEN
    assert isinstance(resultat, (int, float))
    assert resultat == 0.0


def test_calculer_duree_totale_ok():
    """Durée totale correcte pour un utilisateur existant"""

    # GIVEN
    id_utilisateur = 991
    service = ServiceStatistiques()

    # WHEN
    resultat = service.calculer_duree_totale(id_utilisateur)

    # THEN
    assert isinstance(resultat, int)
    assert resultat >= 0


def test_calculer_duree_totale_ko():
    """Durée totale pour un utilisateur sans activité"""

    # GIVEN
    id_utilisateur = 9999
    service = ServiceStatistiques()

    # WHEN
    resultat = service.calculer_duree_totale(id_utilisateur)

    # THEN
    assert isinstance(resultat, int)
    assert resultat == 0

def test_calculer_nombre_activites_semaine_ok():
    """Nombre d'activités par sport correct pour une semaine donnée"""

    # GIVEN
    id_utilisateur = 991
    date_reference = date.today()
    service = ServiceStatistiques()

    # WHEN
    resultat = service.calculer_nombre_activites_semaine(id_utilisateur, date_reference)

    # THEN
    assert isinstance(resultat, dict)
    if resultat:
        assert all(isinstance(k, str) for k in resultat.keys())
        assert all(isinstance(v, int) for v in resultat.values())
    else:
        assert resultat == {}


def test_calculer_nombre_activites_semaine_ko():
    """Aucune activité pour un utilisateur inexistant"""

    # GIVEN
    id_utilisateur = 9999
    date_reference = date.today()
    service = ServiceStatistiques()

    # WHEN
    resultat = service.calculer_nombre_activites_semaine(id_utilisateur, date_reference)

    # THEN
    assert isinstance(resultat, dict)
    assert resultat == {}


def test_calculer_distance_semaine_ok():
    """Distance hebdomadaire correcte pour un utilisateur existant"""

    # GIVEN
    id_utilisateur = 991
    date_reference = date.today()
    service = ServiceStatistiques()

    # WHEN
    resultat = service.calculer_distance_semaine(id_utilisateur, date_reference)

    # THEN
    assert isinstance(resultat, (int, float))
    assert resultat >= 0.0


def test_calculer_distance_semaine_ko():
    """Distance hebdomadaire pour un utilisateur sans activité"""

    # GIVEN
    id_utilisateur = 9999
    date_reference = date.today()
    service = ServiceStatistiques()

    # WHEN
    resultat = service.calculer_distance_semaine(id_utilisateur, date_reference)

    # THEN
    assert isinstance(resultat, (int, float))
    assert resultat == 0.0


def test_calculer_duree_semaine_ok():
    """Durée hebdomadaire correcte pour un utilisateur existant"""

    # GIVEN
    id_utilisateur = 991
    date_reference = date.today()
    service = ServiceStatistiques()

    # WHEN
    resultat = service.calculer_duree_semaine(id_utilisateur, date_reference)

    # THEN
    assert isinstance(resultat, int)
    assert resultat >= 0


def test_calculer_duree_semaine_ko():
    """Durée hebdomadaire pour un utilisateur sans activité"""

    # GIVEN
    id_utilisateur = 9999
    date_reference = date.today()
    service = ServiceStatistiques()

    # WHEN
    resultat = service.calculer_duree_semaine(id_utilisateur, date_reference)

    # THEN
    assert isinstance(resultat, int)
    assert resultat == 0
