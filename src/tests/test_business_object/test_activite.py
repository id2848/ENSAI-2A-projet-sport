from datetime import date, timedelta
from business_object.activite import Activite  


def test_calculer_vitesse_ok():
    """Calcul de la vitesse avec des valeurs normales"""
    # GIVEN
    activite = Activite(
        id_activite=1,
        id_utilisateur=1,
        sport="Sport",
        date_activite=date(2025, 1, 15),
        distance=10.0,
        duree=timedelta(hours=1)
    )

    # WHEN
    res = activite.calculer_vitesse()

    # THEN
    assert res == 10.0


def test_duree_zero_ok():
    """Durée nulle renvoie une vitesse égale à 0.0"""
    activite = Activite(
        id_activite=6,
        id_utilisateur=1,
        sport="Sport",
        date_activite=date(2025, 1, 15),
        distance=10.0,
        duree=timedelta(seconds=0)
    )
    assert activite.calculer_vitesse() == 0.0


def test_distance_zero_ok():
    """Distance nulle renvoie une vitesse égale à 0.0"""
    activite = Activite(
        id_activite=7,
        id_utilisateur=1,
        sport="Sport",
        date_activite=date(2025, 1, 15),
        distance=0.0,
        duree=timedelta(seconds=2000)
    )
    assert activite.calculer_vitesse() == 0.0


def test_distance_et_duree_zeros_ok():
    """Distance et durée nulles renvoient une vitesse égale à 0.0"""
    activite = Activite(
        id_activite=8,
        id_utilisateur=1,
        sport="Sport",
        date_activite=date(2025, 1, 15),
        distance=0.0,
        duree=timedelta(seconds=0)
    )
    assert activite.calculer_vitesse() == 0.0


def test_calculer_vitesse_ko():
    """Vitesse différente de la valeur correcte"""
    activite = Activite(
        id_activite=2,
        id_utilisateur=1,
        sport="Sport",
        date_activite=date(2025, 1, 15),
        distance=10.0,
        duree=timedelta(hours=1)
    )
    assert activite.calculer_vitesse() != 5.0


def test_duree_zero_ko():
    """Durée nulle ne doit pas donner une vitesse positive"""
    activite = Activite(
        id_activite=9,
        id_utilisateur=1,
        sport="Sport",
        date_activite=date(2025, 1, 15),
        distance=10.0,
        duree=timedelta(seconds=0)
    )
    assert activite.calculer_vitesse() != 1.0


def test_distance_zero_ko():
    """Distance nulle ne doit pas donner une vitesse positive"""
    activite = Activite(
        id_activite=10,
        id_utilisateur=1,
        sport="Sport",
        date_activite=date(2025, 1, 15),
        distance=0.0,
        duree=timedelta(seconds=2000)
    )
    assert activite.calculer_vitesse() != 1.0
