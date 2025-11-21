import os
import pytest
from unittest.mock import patch
from utils.reset_database import ResetDatabase

from business_object.abonnement import Abonnement
from dao.abonnement_dao import AbonnementDao

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Initialisation des données de test dans le schéma dédié aux tests"""
    with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
        ResetDatabase().lancer(test_dao=True)
        yield


def test_creer_abonnement_ok():
    """Test de création d'un abonnement réussi"""

    # GIVEN
    id_u_suiveur = 991
    id_u_suivi = 993
    abonnement = Abonnement(id_utilisateur_suiveur=id_u_suiveur, id_utilisateur_suivi=id_u_suivi)

    # WHEN
    creation_ok = AbonnementDao().creer(abonnement)

    # THEN
    assert creation_ok


def test_creer_abonnement_ko():
    """Test de création d'un abonnement échouée"""

    # GIVEN
    id_u_suiveur, id_u_suivi = 123, 100 # non existants
    abonnement = Abonnement(id_utilisateur_suiveur=id_u_suiveur, id_utilisateur_suivi=id_u_suivi)

    # WHEN / THEN
    with pytest.raises(Exception):
        creation_ok = AbonnementDao().creer(abonnement)


def test_trouver_par_ids():
    """Test de la méthode trouver_par_ids"""

    # GIVEN
    id_suiveur = 992
    id_suivi = 991

    # wHEN
    abonnement_trouve = AbonnementDao().trouver_par_ids(id_suiveur, id_suivi)

    # THEN
    assert abonnement_trouve is not None


def test_lister_utilisateurs_suivis_succes():
    """Lister les utilisateurs suivis"""

    # GIVEN
    id = 992

    # WHEN
    res = AbonnementDao().lister_suivis(id)

    # THEN
    ids_suivis = [a.id_utilisateur_suivi for a in res]
    assert set(ids_suivis) == set([991, 993, 994])


def test_lister_utilisateurs_suiveurs_succes():
    """Lister les utilisateurs suivis"""

    # GIVEN
    id = 994

    # WHEN
    res = AbonnementDao().lister_suiveurs(id)

    # THEN
    ids_suiveurs = [a.id_utilisateur_suiveur for a in res]
    assert set(ids_suiveurs) == set([992, 993])


def test_lister_tous():
    """Test de la méthode lister_tous"""

    # GIVEN

    # WHEN
    abonnements = AbonnementDao().lister_tous()

    # THEN
    assert len(abonnements) == 7 # d'après données test


def test_supprimer_abonnement_ok():
    """Test de suppression d'un abonnement réussi"""

    # GIVEN
    id_utilisateur_suiveur = 991
    id_utilisateur_suivi = 992

    # WHEN
    suppression_ok = AbonnementDao().supprimer(id_utilisateur_suiveur, id_utilisateur_suivi)

    # THEN
    assert suppression_ok


def test_supprimer_abonnement_ko():
    """Test de suppression d'un abonnement échouée"""

    # GIVEN
    id_utilisateur_suiveur = 991
    id_utilisateur_suivi = 995

    # WHEN / THEN
    with pytest.raises(Exception):
        suppression_ok = AbonnementDao().supprimer(id_utilisateur_suiveur, id_utilisateur_suivi)


if __name__ == "__main__":
    pytest.main([__file__])
