import os
import pytest
from unittest.mock import patch
from utils.reset_database import ResetDatabase

from service.fil_dactualite_service import Fildactualite

from datetime import date


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Initialisation des données de test dans le schéma dédié aux tests"""
    with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
        ResetDatabase().lancer(test_dao=True)
        yield


def test_creer_fil_dactualite_ok():
    """Création de Fil d'actualité réussie"""

    # GIVEN
    id_utilisateur = 992  # suiveur

    # WHEN
    fil = Fildactualite().creer_fil_dactualite(id_utilisateur)

    # THEN
    # 3 utilisateurs suivis : 991 (3 activités), 993 (1), 994 (1)
    assert isinstance(fil, list)
    assert len(fil) == 5

    # Vérifie que les dates sont triées
    dates = [a.date_activite for a in fil]
    assert dates == sorted(dates, reverse=True)
    assert (
        dates[0] >= dates[4]
    )  # la première doit être la plus récente (date la plus grande)

    # Vérifie les types et contenus
    for activite in fil:
        assert isinstance(activite.date_activite, date)


if __name__ == "__main__":
    pytest.main([__file__])
