import os
import pytest
from unittest.mock import patch

from utils.reset_database import ResetDatabase
from dao.activite_dao import ActiviteDAO
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
        id_activite=1002,
        id_utilisateur=99999,  # utilisateur inexistant
        sport="Natation",
        date_activite="2024-10-10",
        distance=1.2,
        duree=30
    )

    # WHEN
    creation_ok = ActiviteDAO().creer(activite)

    # THEN
    assert not creation_ok


def test_lister_par_utilisateur_ok():
    """Lister les activités d’un utilisateur existant"""

    # GIVEN
    id_utilisateur = 991

    # WHEN
    activites = ActiviteDAO().lister_par_utilisateur(id_utilisateur)

    # THEN
    assert isinstance(activites, list)
    for a in activites:
        assert isinstance(a, Activite)
        assert a.id_utilisateur == id_utilisateur


def test_lister_par_utilisateur_vide():
    """Lister les activités d’un utilisateur sans activité"""

    # GIVEN
    id_utilisateur = 9999  # id sans activité

    # WHEN
    activites = ActiviteDAO().lister_par_utilisateur(id_utilisateur)

    # THEN
    assert isinstance(activites, list)
    assert len(activites) == 0



def test_trouver_par_id_ko():
    """Trouver un utilisateur inexistant via l'id_utilisateur"""

    # GIVEN
    id_utilisateur = 9999

    # WHEN
    utilisateur = ActiviteDAO().trouver_par_id(id_utilisateur)

    # THEN
    assert utilisateur is None
