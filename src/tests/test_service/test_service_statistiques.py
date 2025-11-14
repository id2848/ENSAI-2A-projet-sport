import os
import pytest
from unittest.mock import patch

from utils.reset_database import ResetDatabase
from dao.activite_dao import ActiviteDao
from business_object.activite import Activite
from service.service_statistiques import ServiceStatistiques


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialisation des données de test dans le schéma dédié aux tests"""
    with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
        ResetDatabase().lancer(test_dao=True)
        yield

def test_verifier_utilisateur_existant():
    """Test pour vérifier si un utilisateur existe"""
    
    # GIVEN
    id_existant = 992  # Utilisateur avec ID 992 existe dans la base
    id_inexistant = 9999999  # Utilisateur qui n'existe pas
    
    # WHEN / THEN
    assert ServiceStatistiques().verifier_utilisateur_existant(id_existant) is True
    assert ServiceStatistiques().verifier_utilisateur_existant(id_inexistant) is False

def test_verifier_date():
    """Test pour vérifier si la date est au bon format"""
    
    # GIVEN
    date_valide = "2025-09-26"
    date_invalide = "26-09-2025"  # Format incorrect
    
    # WHEN / THEN
    assert ServiceStatistiques().verifier_date(date_valide) is True
    assert ServiceStatistiques().verifier_date(date_invalide) is False

def test_calculer_nombre_activites_total():
    """Test pour calculer le nombre total d'activités par sport"""
    
    # GIVEN
    id_utilisateur = 992  # Utilisateur existant dans la base
    
    # WHEN
    stats = ServiceStatistiques().calculer_nombre_activites_total(id_utilisateur)
    
    # THEN
    assert stats == {'natation': 1}  # 1 activité de natation pour l'utilisateur 992

def test_calculer_distance_totale():
    """Test pour calculer la distance totale parcourue par l'utilisateur"""
    
    # GIVEN
    id_utilisateur = 992  # Utilisateur existant
    
    # WHEN
    distance_totale = ServiceStatistiques().calculer_distance_totale(id_utilisateur)
    
    # THEN
    assert distance_totale == 2.5  # La distance de l'utilisateur 992 est 2.5 km pour la natation

def test_calculer_duree_totale():
    """Test pour calculer la durée totale des activités de l'utilisateur"""
    
    # GIVEN
    id_utilisateur = 992  # Utilisateur existant
    
    # WHEN
    duree_totale = ServiceStatistiques().calculer_duree_totale(id_utilisateur)
    
    # THEN
    assert duree_totale == 2700  # Durée totale = 45 minutes * 60 secondes = 2700 secondes

def test_calculer_nombre_activites_semaine():
    """Test pour calculer le nombre d'activités par sport dans une semaine donnée"""
    
    # GIVEN
    id_utilisateur = 992  # Utilisateur existant
    date_reference = "2025-09-26"  # Date dans la semaine
    
    # WHEN
    stats = ServiceStatistiques().calculer_nombre_activites_semaine(id_utilisateur, date_reference)
    
    # THEN
    assert stats == {'natation': 1}  # 1 activité de natation dans la semaine du 26 septembre

def test_calculer_distance_semaine():
    """Test pour calculer la distance totale parcourue dans la semaine"""
    
    # GIVEN
    id_utilisateur = 992  # Utilisateur existant
    date_reference = "2025-09-26"  # Date dans la semaine
    
    # WHEN
    distance_semaine = ServiceStatistiques().calculer_distance_semaine(id_utilisateur, date_reference)
    
    # THEN
    assert distance_semaine == 2.5  # 2.5 km pour l'activité de natation cette semaine

def test_calculer_duree_semaine():
    """Test pour calculer la durée totale des activités dans la semaine"""
    
    # GIVEN
    id_utilisateur = 992  # Utilisateur existant
    date_reference = "2025-09-26"  # Date dans la semaine
    
    # WHEN
    duree_semaine = ServiceStatistiques().calculer_duree_semaine(id_utilisateur, date_reference)
    
    # THEN
    assert duree_semaine == 2700  # Durée totale pour l'activité de natation = 45 minutes = 2700 secondes
