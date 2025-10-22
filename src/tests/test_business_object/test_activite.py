import unittest
from datetime import date, timedelta
from business_object.activite import Activite  

class TestActiviteCalculerVitesse(unittest.TestCase):
    """Tests unitaires pour la méthode calculer_vitesse de la classe Activite."""

    def setUp(self):
        """Préparation avant chaque test."""
        self.sport_test = "Course"  
    
    def test_calculer_vitesse(self):
        """Test avec des valeurs normales : 10 km en 1 heure = 10 km/h."""
        activite = Activite(
            id_activite=1,
            id_utilisateur=1,
            sport=self.sport_test,
            date_activite=date(2025, 1, 15),
            distance=10.0,
            duree=timedelta(hours=1)
        )
        self.assertEqual(activite.calculer_vitesse(), 10.0)
    
   
    
    def test_duree_zero(self):
        """Test avec durée nulle : devrait retourner 0.0."""
        activite = Activite(
            id_activite=6,
            id_utilisateur=1,
            sport=self.sport_test,
            date_activite=date(2025, 1, 15),
            distance=10.0,
            duree=timedelta(seconds=0)
        )
        self.assertEqual(activite.calculer_vitesse(), 0.0)
    
    def test_distance_zero(self):
        """Test avec distance nulle : devrait retourner 0.0."""
        activite = Activite(
            id_activite=7,
            id_utilisateur=1,
            sport=self.sport_test,
            date_activite=date(2025, 1, 15),
            distance=0.0,
            duree=timedelta(seconds=2000)
        )
        self.assertEqual(activite.calculer_vitesse(), 0.0)
    
    def test_distance_et_duree_zeros(self):
        """Test avec distance et durée nulles : devrait retourner 0.0."""
        activite = Activite(
            id_activite=8,
            id_utilisateur=1,
            sport=self.sport_test,
            date_activite=date(2025, 1, 15),
            distance=0.0,
            duree=timedelta(seconds=0)
        )
        self.assertEqual(activite.calculer_vitesse(), 0.0)
    