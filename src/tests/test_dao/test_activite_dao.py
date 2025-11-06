import os
import pytest
from unittest.mock import patch
from datetime import datetime

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
    assert activite.id_activite


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
    id_activite = 991

    # WHEN
    activite = ActiviteDao().trouver_par_id(id_activite)

    # THEN
    assert activite is not None
    assert activite.id_activite == id_activite


def test_modifier_ok():
    """Modification d'une activité existante réussie"""
    # GIVEN
    activite = Activite(
        id_activite=995,
        id_utilisateur=995,
        sport="randonnée",
        date_activite="2025-09-29",
        distance=10.0,
        duree=50.0
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
        id_activite=994,
        id_utilisateur=994,
        sport="randonnée",
        date_activite="2025-09-28",
        distance=10.0,
        duree=120.0
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

def test_lister_activites_filtres_par_sport():
    """Lister les activités d’un utilisateur filtrées par sport"""
    # GIVEN
    id_utilisateur = 991
    sport_filtre = "natation"  # Exemple de filtre

    # WHEN
    activites = ActiviteDao().lister_activites_filtres(id_utilisateur, sport=sport_filtre)

    # THEN
    assert isinstance(activites, list)
    for a in activites:
        assert isinstance(a, Activite)
        assert a.sport == sport_filtre

def test_lister_activites_filtres_par_date():
    """Lister les activités d’un utilisateur filtrées par plage de dates"""
    # GIVEN
    id_utilisateur = 991
    date_debut = "2025-01-01"
    date_fin = "2025-12-31"
    # Convertir les dates en objets datetime.date
    date_debut = datetime.strptime(date_debut, "%Y-%m-%d").date()
    date_fin = datetime.strptime(date_fin, "%Y-%m-%d").date()
    # WHEN
    activites = ActiviteDao().lister_activites_filtres(id_utilisateur, date_debut=date_debut, date_fin=date_fin)

    # THEN
    assert isinstance(activites, list)
    for a in activites:
        assert isinstance(a, Activite)
        assert date_debut <= a.date_activite <= date_fin

def test_lister_activites_filtres_par_sport_et_date():
    """Lister les activités d’un utilisateur filtrées par sport et plage de dates"""
    # GIVEN
    id_utilisateur = 991
    sport_filtre = "natation"
    date_debut = "2025-01-01"
    date_fin = "2025-12-31"
    # Convertir les dates en objets datetime.date
    date_debut = datetime.strptime(date_debut, "%Y-%m-%d").date()
    date_fin = datetime.strptime(date_fin, "%Y-%m-%d").date()
    # WHEN
    activites = ActiviteDao().lister_activites_filtres(id_utilisateur, sport=sport_filtre, date_debut=date_debut, date_fin=date_fin)

    # THEN
    assert isinstance(activites, list)
    for a in activites:
        assert isinstance(a, Activite)
        assert a.sport == sport_filtre
        assert date_debut <= a.date_activite <= date_fin

def test_lister_activites_filtres_sans_filtre():
    """Lister toutes les activités d’un utilisateur sans appliquer de filtres"""
    # GIVEN
    id_utilisateur = 991

    # WHEN
    activites = ActiviteDao().lister_activites_filtres(id_utilisateur)

    # THEN
    assert isinstance(activites, list)
    for a in activites:
        assert isinstance(a, Activite)
        assert a.id_utilisateur == id_utilisateur
