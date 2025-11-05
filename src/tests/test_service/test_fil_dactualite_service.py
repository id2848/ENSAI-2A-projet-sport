
from service.fil_dactualite_service import Fildactualite

from dao.abonnement_dao import AbonnementDao
from dao.utilisateur_dao import UtilisateurDao
from dao.activite_dao import ActiviteDao


from business_object.abonnement import Abonnement
from business_object.utilisateur import Utilisateur
from business_object.activite import Activite

from datetime import date, timedelta

import os
import pytest
from unittest.mock import patch
from utils.reset_database import ResetDatabase

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialisation des données de test dans le schéma dédié aux tests"""
    with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
        ResetDatabase().lancer(test_dao=True)
        yield

def test_creer_fil_dactualite_ok():
    """ "Création de Fil d'actualité réussie"""

 

    # GIVEN
    id_utilisateur = 991  # utilisateur suiveur
    # Les utilisateurs suivis (992 à 995) ont déjà des activités dans la base :
    # (992, 'natation', 2025-09-26), (993, 'vélo', 2025-09-27), etc.


    # WHEN
    fil = Fildactualite().creer_fil_dactualite(id_utilisateur)

    # THEN
    assert isinstance(fil, list)
    assert len(fil) == 1  # 4 activités des suivis (992 à 995)
    
    # Vérifie que les dates sont triées
    dates = [a.date_activite for a in fil]
    assert dates == sorted(dates)

    # Vérifie les types et contenus
    for activite in fil:
        assert activite.sport in ['natation', 'vélo', 'randonnée', 'course']
        assert isinstance(activite.date_activite, date)