import pytest
from unittest.mock import MagicMock
from datetime import datetime
from business_object.activite import Activite
from business_object.commentaire import Commentaire
from business_object.utilisateur import Utilisateur
from business_object.jaime import Jaime
from service.activite_service import ActiviteService

# Fixtures
@pytest.fixture
def activite_service():
    return ActiviteService()

@pytest.fixture
def mock_activite_dao():
    mock_dao = MagicMock()
    return mock_dao

@pytest.fixture
def mock_utilisateur_dao():
    mock_dao = MagicMock()
    return mock_dao

@pytest.fixture
def mock_commentaire_dao():
    mock_dao = MagicMock()
    return mock_dao

@pytest.fixture
def mock_jaime_dao():
    mock_dao = MagicMock()
    return mock_dao

# Tests des méthodes de ActiviteService

def test_creer_activite(activite_service, mock_activite_dao):
    """Test de la création d'une activité"""
    # Configuration du mock
    mock_activite_dao.creer.return_value = True

    # Test
    result = activite_service.creer_activite(id_utilisateur=1, sport="course")
    
    # Vérification
    assert result is True
    mock_activite_dao.creer.assert_called_once()

def test_supprimer_activite(activite_service, mock_activite_dao):
    """Test de la suppression d'une activité"""
    # Configuration du mock
    mock_activite_dao.trouver_par_id.return_value = Activite(id_utilisateur=1, sport="course", date_activite=datetime.now())
    mock_activite_dao.supprimer.return_value = True
    
    # Test
    result = activite_service.supprimer_activite(id_activite=1)
    
    # Vérification
    assert result is True
    mock_activite_dao.supprimer.assert_called_once()

def test_modifier_activite(activite_service, mock_activite_dao):
    """Test de la modification d'une activité"""
    # Configuration du mock
    mock_activite_dao.trouver_par_id.return_value = Activite(id_utilisateur=1, sport="course", date_activite=datetime.now())
    
    # Test
    result = activite_service.modifier_activite(id_activite=1, sport="marche")
    
    # Vérification
    assert result is True
    mock_activite_dao.modifier.assert_called_once()

def test_lister_activites(activite_service, mock_activite_dao):
    """Test de la liste des activités d'un utilisateur"""
    # Configuration du mock
    mock_activite_dao.lister_par_utilisateur.return_value = [Activite(id_utilisateur=1, sport="course", date_activite=datetime.now())]
    
    # Test
    result = activite_service.lister_activites(id_utilisateur=1)
    
    # Vérification
    assert len(result) > 0
    mock_activite_dao.lister_par_utilisateur.assert_called_once()

def test_ajouter_jaime(activite_service, mock_jaime_dao, mock_activite_dao, mock_utilisateur_dao):
    """Test de l'ajout d'un 'j'aime' à une activité"""
    # Configuration du mock
    mock_activite_dao.trouver_par_id.return_value = Activite(id_utilisateur=1, sport="course", date_activite=datetime.now())
    mock_utilisateur_dao.trouver_par_id.return_value = Utilisateur(id_utilisateur=1, pseudo="User1")
    
    # Test
    result = activite_service.ajouter_jaime(id_activite=1, id_utilisateur=1)
    
    # Vérification
    assert result is True
    mock_jaime_dao.creer.assert_called_once()

def test_supprimer_jaime(activite_service, mock_jaime_dao, mock_activite_dao, mock_utilisateur_dao):
    """Test de la suppression d'un 'j'aime' d'une activité"""
    # Configuration du mock
    mock_activite_dao.trouver_par_id.return_value = Activite(id_utilisateur=1, sport="course", date_activite=datetime.now())
    mock_utilisateur_dao.trouver_par_id.return_value = Utilisateur(id_utilisateur=1, pseudo="User1")
    
    # Test
    result = activite_service.supprimer_jaime(id_utilisateur=1, id_activite=1)
    
    # Vérification
    assert result is True
    mock_jaime_dao.supprimer.assert_called_once()

def test_ajouter_commentaire(activite_service, mock_commentaire_dao, mock_activite_dao, mock_utilisateur_dao):
    """Test de l'ajout d'un commentaire à une activité"""
    # Configuration du mock
    mock_activite_dao.trouver_par_id.return_value = Activite(
    id_activite=1,  # Id de l'activité
    id_utilisateur=1,
    sport="course",
    date_activite=datetime.now(),
    distance=10.5,  # Distance de l'activité
    duree=timedelta(hours=1)  # Durée de l'activité
)
    mock_utilisateur_dao.trouver_par_id.return_value = Utilisateur(id_utilisateur=1, pseudo="User1")
    
    # Test
    result = activite_service.ajouter_commentaire(id_utilisateur=1, id_activite=1, commentaire="super!")
    
    # Vérification
    assert result is True
    mock_commentaire_dao.creer.assert_called_once()

def test_supprimer_commentaire(activite_service, mock_commentaire_dao):
    """Test de la suppression d'un commentaire"""
    # Configuration du mock
    mock_commentaire_dao.trouver_par_id.return_value = Commentaire(id_utilisateur=1, id_activity=1, commentaire="super!", date_commentaire=datetime.now())
    
    # Test
    result = activite_service.supprimer_commentaire(id_commentaire=1)
    
    # Vérification
    assert result is True
    mock_commentaire_dao.supprimer.assert_called_once()

def test_lister_commentaires(activite_service, mock_commentaire_dao):
    """Test de la liste des commentaires d'une activité"""
    # Configuration du mock
    mock_commentaire_dao.lister_par_activite.return_value = [Commentaire(id_utilisateur=1, id_activity=1, commentaire="pas mal!", date_commentaire=datetime.now())]
    
    # Test
    result = activite_service.lister_commentaires(id_activite=1)
    
    # Vérification
    assert len(result) > 0
    mock_commentaire_dao.lister_par_activite.assert_called_once()

