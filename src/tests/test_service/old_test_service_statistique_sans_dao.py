from unittest.mock import MagicMock
from datetime import timedelta, date

from business_object.activite import Activite
from service.statistiques_service import StatistiquesService


liste_activites = [
    Activite(
        id_activite=1,
        id_utilisateur=1,
        sport="Course",
        date_activite=date(2025, 1, 1),
        distance=5.0,
        duree=timedelta(minutes=30),
    ),
    Activite(
        id_activite=2,
        id_utilisateur=1,
        sport="Course",
        date_activite=date(2025, 1, 2),
        distance=10.0,
        duree=timedelta(hours=1),
    ),
    Activite(
        id_activite=3,
        id_utilisateur=2,
        sport="Natation",
        date_activite=date(2025, 1, 3),
        distance=7.0,
        duree=timedelta(minutes=45),
    ),
]

statistiques_service = StatistiquesService()
statistiques_service.activite_dao = MagicMock()


def test_calculer_nombre_activites_ok():
    """Nombre d'activités correct pour un utilisateur existant"""
    # GIVEN
    statistiques_service.activite_dao.lister_par_utilisateur = MagicMock(
        return_value=[a for a in liste_activites if a.id_utilisateur == 1]
    )

    # WHEN
    res = statistiques_service.calculer_nombre_activites(1)

    # THEN
    assert res == 2


def test_calculer_nombre_activites_ko():
    """Nombre d'activités pour un utilisateur sans activité"""
    # GIVEN
    statistiques_service.activite_dao.lister_par_utilisateur = MagicMock(
        return_value=[]
    )

    # WHEN
    res = statistiques_service.calculer_nombre_activites(99)

    # THEN
    assert res == 0


def test_calculer_distance_totale_ok():
    """Distance totale correcte pour un utilisateur existant"""
    # GIVEN
    statistiques_service.activite_dao.lister_par_utilisateur = MagicMock(
        return_value=[a for a in liste_activites if a.id_utilisateur == 1]
    )

    # WHEN
    res = statistiques_service.calculer_distance_totale(1)

    # THEN
    assert res == 15.0


def test_calculer_distance_totale_ko():
    """Distance totale pour un utilisateur sans activité"""
    # GIVEN
    statistiques_service.activite_dao.lister_par_utilisateur = MagicMock(
        return_value=[]
    )

    # WHEN
    res = statistiques_service.calculer_distance_totale(99)

    # THEN
    assert res == 0.0


def test_calculer_duree_totale_ok():
    """Durée totale correcte pour un utilisateur existant"""
    # GIVEN
    statistiques_service.activite_dao.lister_par_utilisateur = MagicMock(
        return_value=[a for a in liste_activites if a.id_utilisateur == 1]
    )
    total_sec = int(
        timedelta(minutes=30).total_seconds() + timedelta(hours=1).total_seconds()
    )

    # WHEN
    res = statistiques_service.calculer_duree_totale(1)

    # THEN
    assert res == total_sec


def test_calculer_duree_totale_ko():
    """Durée totale pour un utilisateur sans activité"""
    # GIVEN
    statistiques_service.activite_dao.lister_par_utilisateur = MagicMock(
        return_value=[]
    )

    # WHEN
    res = statistiques_service.calculer_duree_totale(99)

    # THEN
    assert res == 0


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
