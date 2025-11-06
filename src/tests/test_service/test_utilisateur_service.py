import pytest
from datetime import date, timedelta
from service.utilisateur_service import UtilisateurService
from dao.utilisateur_dao import UtilisateurDao
from business_object.utilisateur import Utilisateur

import os
from unittest.mock import patch
from utils.reset_database import ResetDatabase

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Initialisation des données de test dans la base de données"""
    # Assurez-vous d'utiliser un schéma de test pour éviter de modifier la vraie base de données
    with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
        # Reset de la base de données avant de commencer
        ResetDatabase().lancer(test_dao=True)
        yield

def test_lister_utilisateurs():
    """Test pour lister tous les utilisateurs"""

    # GIVEN
    # WHEN
    liste = UtilisateurService().lister_utilisateurs()

    # THEN
    assert len(liste) > 1


def test_trouver_par_id_ok():
    """Recherche par id d'un utilisateur existant"""

    # GIVEN
    id = 995

    # WHEN
    utilisateur = UtilisateurService().trouver_par_id(id)

    # THEN
    assert utilisateur is not None

def test_trouver_par_id_ko():
    """Recherche par id d'un utilisateur n'existant pas"""

    # GIVEN
    id = 606

    # WHEN
    utilisateur = UtilisateurService().trouver_par_id(id)

    # THEN
    assert utilisateur is None

def test_trouver_par_pseudo_ok():
    """Recherche par pseudo d'un utilisateur existant"""

    # GIVEN
    pseudo = 'mikebrown'

    # WHEN
    utilisateur = UtilisateurService().trouver_par_pseudo(pseudo)

    # THEN
    assert utilisateur is not None

def test_trouver_par_pseudo_ko():
    """Recherche par pseudo d'un utilisateur existant"""

    # GIVEN
    pseudo = 'pppppp'

    # WHEN
    utilisateur = UtilisateurService().trouver_par_pseudo(pseudo)

    # THEN
    assert utilisateur is None

if __name__ == "__main__":
    import pytest
    pytest.main([__file__])

