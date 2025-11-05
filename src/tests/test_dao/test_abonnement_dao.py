import os
import pytest

from unittest.mock import patch, MagicMock

from utils.reset_database import ResetDatabase
from utils.securite import hash_password
from business_object.abonnement import Abonnement
from dao.abonnement_dao import AbonnementDao

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialisation des données de test"""
    with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
        # Reset la base de données ou effectue toute autre initialisation si nécessaire
        yield


def test_creer_abonnement_ok():
    """Test de création d'un abonnement réussi"""

    # GIVEN
    abonnement = Abonnement(id_utilisateur_suiveur=1, id_utilisateur_suivi=2)

    # Simuler l'exécution de la méthode de création
    with patch.object(AbonnementDao, 'creer', return_value=True) as mock_creer:
        creation_ok = AbonnementDao().creer(abonnement)

    # WHEN
    # THEN
    assert creation_ok
    mock_creer.assert_called_once_with(abonnement)


def test_creer_abonnement_ko():
    """Test de création d'un abonnement échouée"""

    # GIVEN
    abonnement = Abonnement(id_utilisateur_suiveur=1, id_utilisateur_suivi="non_int")

    # Simuler l'échec de la méthode de création (faux type)
    with patch.object(AbonnementDao, 'creer', return_value=False) as mock_creer:
        creation_ok = AbonnementDao().creer(abonnement)

    # WHEN
    # THEN
    assert not creation_ok
    mock_creer.assert_called_once_with(abonnement)


def test_trouver_par_ids():
    """Test de la méthode trouver_par_ids"""

    # GIVEN
    id_suiveur = 1
    id_suivi = 2
    mock_abonnement = Abonnement(id_utilisateur_suiveur=id_suiveur, id_utilisateur_suivi=id_suivi)

    with patch.object(AbonnementDao, 'trouver_par_ids', return_value=mock_abonnement) as mock_trouver:
        abonnement_trouve = AbonnementDao().trouver_par_ids(id_suiveur, id_suivi)

    # WHEN
    # THEN
    assert abonnement_trouve == mock_abonnement
    mock_trouver.assert_called_once_with(id_suiveur, id_suivi)


def test_lister_suivis():
    """Test de la méthode lister_suivis"""

    # GIVEN
    id_utilisateur = 1
    mock_abonnements = [
        Abonnement(id_utilisateur_suiveur=id_utilisateur, id_utilisateur_suivi=2),
        Abonnement(id_utilisateur_suiveur=id_utilisateur, id_utilisateur_suivi=3),
    ]
    
    with patch.object(AbonnementDao, 'lister_suivis', return_value=mock_abonnements) as mock_lister:
        abonnements = AbonnementDao().lister_suivis(id_utilisateur)

    # WHEN
    # THEN
    assert len(abonnements) == 2
    assert abonnements[0].id_utilisateur_suiveur == id_utilisateur
    mock_lister.assert_called_once_with(id_utilisateur)


def test_lister_suiveurs():
    """Test de la méthode lister_suiveurs"""

    # GIVEN
    id_utilisateur = 2
    mock_abonnements = [
        Abonnement(id_utilisateur_suiveur=1, id_utilisateur_suivi=id_utilisateur),
        Abonnement(id_utilisateur_suiveur=3, id_utilisateur_suivi=id_utilisateur),
    ]
    
    with patch.object(AbonnementDao, 'lister_suiveurs', return_value=mock_abonnements) as mock_lister:
        abonnements = AbonnementDao().lister_suiveurs(id_utilisateur)

    # WHEN
    # THEN
    assert len(abonnements) == 2
    assert abonnements[0].id_utilisateur_suivi == id_utilisateur
    mock_lister.assert_called_once_with(id_utilisateur)


def test_lister_tous():
    """Test de la méthode lister_tous"""

    # GIVEN
    mock_abonnements = [
        Abonnement(id_utilisateur_suiveur=1, id_utilisateur_suivi=2),
        Abonnement(id_utilisateur_suiveur=1, id_utilisateur_suivi=3),
    ]
    
    with patch.object(AbonnementDao, 'lister_tous', return_value=mock_abonnements) as mock_lister:
        abonnements = AbonnementDao().lister_tous()

    # WHEN
    # THEN
    assert len(abonnements) == 2
    mock_lister.assert_called_once()


def test_supprimer_abonnement_ok():
    """Test de suppression d'un abonnement réussi"""

    # GIVEN
    abonnement = Abonnement(id_utilisateur_suiveur=1, id_utilisateur_suivi=2)

    with patch.object(AbonnementDao, 'supprimer', return_value=True) as mock_supprimer:
        suppression_ok = AbonnementDao().supprimer(abonnement)

    # WHEN
    # THEN
    assert suppression_ok
    mock_supprimer.assert_called_once_with(abonnement)


def test_supprimer_abonnement_ko():
    """Test de suppression d'un abonnement échouée"""

    # GIVEN
    abonnement = Abonnement(id_utilisateur_suiveur=1, id_utilisateur_suivi=999)

    with patch.object(AbonnementDao, 'supprimer', return_value=False) as mock_supprimer:
        suppression_ok = AbonnementDao().supprimer(abonnement)

    # WHEN
    # THEN
    assert not suppression_ok
    mock_supprimer.assert_called_once_with(abonnement)


if __name__ == "__main__":
    pytest.main([__file__])

