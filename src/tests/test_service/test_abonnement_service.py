import os
import pytest
from unittest.mock import patch
from utils.reset_database import ResetDatabase

from service.abonnement_service import AbonnementService

from business_object.abonnement import Abonnement
from business_object.utilisateur import Utilisateur


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
    """Création de Abonnement échouée"""

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

def test_supprimer_abonnement_ok():
    """Test de suppression d'un abonnement réussi"""

    # GIVEN
    id_utilisateur_suiveur=991
    id_utilisateur_suivi=992

    # WHEN
    suppression_ok = AbonnementService().supprimer_abonnement(id_utilisateur_suiveur, id_utilisateur_suivi)

    # THEN
    assert suppression_ok

def test_supprimer_abonnement_ko():
    """Test de suppression d'un abonnement échouée"""

    # GIVEN
    id_utilisateur_suiveur=991
    id_utilisateur_suivi=995

    # WHEN
    suppression_ok = AbonnementService().supprimer_abonnement(id_utilisateur_suiveur, id_utilisateur_suivi)

    # THEN
    assert not suppression_ok


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
