import pytest
from datetime import date, timedelta
from service.activite_service import ActiviteService
from dao.activite_dao import ActiviteDao
from dao.jaime_dao import JaimeDao
from dao.commentaire_dao import CommentaireDao
from dao.utilisateur_dao import UtilisateurDao
from business_object.activite import Activite
from business_object.jaime import Jaime
from business_object.commentaire import Commentaire
from business_object.utilisateur import Utilisateur

import os
from unittest.mock import patch
from utils.reset_database import ResetDatabase

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialisation des données de test dans la base de données"""
    # Assurez-vous d'utiliser un schéma de test pour éviter de modifier la vraie base de données
    with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
        # Reset de la base de données avant de commencer
        ResetDatabase().lancer(test_dao=True)
        yield

def test_creer_activite_ok():
    """Test pour la création d'une activité réussie"""

    # GIVEN
    id_utilisateur = 991  # John Doe
    sport = 'course'
    date_activite = date(2025, 9, 25)  # Date d'activité existante
    distance = 5.0
    duree = timedelta(minutes=30)

    # WHEN
    activite = ActiviteService().creer_activite(id_utilisateur, sport, date_activite, distance, duree)

    # THEN
    # Vérifie que l'activité est créée correctement
    assert activite is True

def test_creer_activite_echec():
    """Test pour la création d'une activité échouée (par exemple, si l'utilisateur n'existe pas)"""

    # GIVEN
    id_utilisateur = 99999999  # Un utilisateur qui n'existe pas
    sport = 'course'
    date_activite = date(2025, 9, 25)
    distance = 5.0
    duree = timedelta(minutes=30)

    # WHEN
    activite = ActiviteService().creer_activite(id_utilisateur, sport, date_activite, distance, duree)

    # THEN
    assert activite is False

def test_lister_activites():
    """Test pour lister les activités d'un utilisateur"""

    # GIVEN
    id_utilisateur = 991  # John Doe

    # WHEN
    activites = ActiviteService().lister_activites(id_utilisateur)

    # THEN
    assert len(activites) == 1
    assert activites[0].sport == 'course'  # L'activité associée à cet utilisateur doit être une course

def test_ajouter_jaime_ok():
    """Test pour l'ajout d'un 'j'aime' à une activité"""

    # GIVEN
    id_activite = 993
    id_utilisateur = 992

    # WHEN
    result = ActiviteService().ajouter_jaime(id_activite, id_utilisateur)

    # THEN
    assert result is True

def test_ajouter_jaime_echec():
    """Test pour l'échec de l'ajout d'un 'j'aime' (par exemple, si l'activité n'existe pas)"""

    # GIVEN
    id_utilisateur = 99999  # Un utilisateur qui n'existe pas
    id_activite = 999  # Une activité qui n'existe pas

    # WHEN
    result = ActiviteService().ajouter_jaime(id_activite, id_utilisateur)

    # THEN
    assert result is False

def test_lister_commentaires():
    """Test pour lister les commentaires d'une activité"""

    # GIVEN
    id_activite = 993  # Activité de Sam Smith

    # WHEN
    commentaires = ActiviteService().lister_commentaires(id_activite)

    # THEN
    assert len(commentaires) == 1
    assert commentaires[0].commentaire == "J'adore le vélo !"  # Le commentaire de Sam

def test_ajouter_commentaire_ok():
    """Test pour ajouter un commentaire à une activité"""

    # GIVEN
    id_utilisateur = 991  # John Doe
    id_activite = 994  # Activité de Emily Jones
    commentaire = "Très belle randonnée !"

    # WHEN
    result = ActiviteService().ajouter_commentaire(id_utilisateur, id_activite, commentaire)

    # THEN
    assert result is True

def test_ajouter_commentaire_echec():
    """Test pour l'échec de l'ajout d'un commentaire (par exemple, si l'activité n'existe pas)"""

    # GIVEN
    id_utilisateur = 999  # Un utilisateur qui n'existe pas
    id_activite = 999  # Une activité qui n'existe pas
    commentaire = "Super activité !"

    # WHEN
    result = ActiviteService().ajouter_commentaire(id_utilisateur, id_activite, commentaire)

    # THEN
    assert result is False

def test_supprimer_activite_ok():
    """Test pour la suppression d'une activité"""

    # GIVEN
    id_activite = 991  # L'activité de John Doe

    # WHEN
    result = ActiviteService().supprimer_activite(id_activite)

    # THEN
    assert result is True

def test_supprimer_activite_echec():
    """Test pour l'échec de la suppression d'une activité (par exemple, si l'activité n'existe pas)"""

    # GIVEN
    id_activite = 999  # Une activité qui n'existe pas

    # WHEN
    result = ActiviteService().supprimer_activite(id_activite)

    # THEN
    assert result is False

if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
