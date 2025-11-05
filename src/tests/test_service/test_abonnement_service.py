
from service.abonnement_service import AbonnementService

from dao.abonnement_dao import AbonnementDao
from dao.utilisateur_dao import UtilisateurDao

from business_object.abonnement import Abonnement
from business_object.utilisateur import Utilisateur

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

def test_creer_ok():
    """ "Création de Abonnement réussie"""

    # GIVEN
    id_u_suiveur= 991
    id_u_suivi=993

    # WHEN
    abonnement = AbonnementService().creer_abonnement(id_u_suiveur, id_u_suivi)

    # THEN
    assert abonnement.id_utilisateur_suiveur == id_u_suiveur and abonnement.id_utilisateur_suivi == id_u_suivi


def test_creer_echec():
    """Création de Abonnement échouée
    (car la méthode AbonnementDao().creer retourne False)"""

    # GIVEN
    id_u_suiveur, id_u_suivi = 123, 100

    # WHEN
    abonnement = AbonnementService().creer_abonnement(id_u_suiveur, id_u_suivi)

    # THEN
    assert abonnement is None


def test_lister_utilisateurs_suivis_succes():
    """Lister les utilisateurs suivis"""

    # GIVEN
    id = 992

    # WHEN
    res = AbonnementService().lister_utilisateurs_suivis(id)

    # THEN
    assert res == set([993, 994, 995, 991])


def test_lister_utilisateurs_suiveurs_succes():
    """Lister les utilisateurs suivis"""

    # GIVEN
    id = 994

    # WHEN
    res = AbonnementService().lister_utilisateurs_suiveurs(id)

    # THEN
    assert res == set([992, 993])


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
