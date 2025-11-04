import unittest
from datetime import date, timedelta
from business_object.activite import Activite  

class TestActiviteCalculerVitesse(unittest.TestCase):
    """Tests unitaires pour la méthode calculer_vitesse de la classe Activite."""

    def setUp(self):
        """Préparation avant chaque test."""
        self.sport_test = "Course"  

    def test_calculer_vitesse_ok(self):
        """OK : Test avec des valeurs normales : 10 km en 1 heure = 10 km/h."""
        activite = Activite(
            id_activite=1,
            id_utilisateur=1,
            sport=self.sport_test,
            date_activite=date(2025, 1, 15),
            distance=10.0,
            duree=timedelta(hours=1)
        )
        self.assertEqual(activite.calculer_vitesse(), 10.0)

    def test_duree_zero_ok(self):
        """OK : Test avec durée nulle : devrait retourner 0.0."""
        activite = Activite(
            id_activite=6,
            id_utilisateur=1,
            sport=self.sport_test,
            date_activite=date(2025, 1, 15),
            distance=10.0,
            duree=timedelta(seconds=0)
        )
        self.assertEqual(activite.calculer_vitesse(), 0.0)

    def test_distance_zero_ok(self):
        """OK : Test avec distance nulle : devrait retourner 0.0."""
        activite = Activite(
            id_activite=7,
            id_utilisateur=1,
            sport=self.sport_test,
            date_activite=date(2025, 1, 15),
            distance=0.0,
            duree=timedelta(seconds=2000)
        )
        self.assertEqual(activite.calculer_vitesse(), 0.0)

    def test_distance_et_duree_zeros_ok(self):
        """OK : Test avec distance et durée nulles : devrait retourner 0.0."""
        activite = Activite(
            id_activite=8,
            id_utilisateur=1,
            sport=self.sport_test,
            date_activite=date(2025, 1, 15),
            distance=0.0,
            duree=timedelta(seconds=0)
        )
        self.assertEqual(activite.calculer_vitesse(), 0.0)

    def test_calculer_vitesse_ko(self):
        """KO : Test incorrect : vérifier que vitesse différente de la vraie valeur échoue."""
        activite = Activite(
            id_activite=2,
            id_utilisateur=1,
            sport=self.sport_test,
            date_activite=date(2025, 1, 15),
            distance=10.0,
            duree=timedelta(hours=1)
        )
        self.assertNotEqual(activite.calculer_vitesse(), 5.0)  # KO attendu

    def test_duree_zero_ko(self):
        """KO : Test incorrect : durée nulle ne devrait pas donner une vitesse > 0."""
        activite = Activite(
            id_activite=9,
            id_utilisateur=1,
            sport=self.sport_test,
            date_activite=date(2025, 1, 15),
            distance=10.0,
            duree=timedelta(seconds=0)
        )
        self.assertNotEqual(activite.calculer_vitesse(), 1.0)  # KO attendu

    def test_distance_zero_ko(self):
        """KO : Test incorrect : distance nulle ne devrait pas donner une vitesse > 0."""
        activite = Activite(
            id_activite=10,
            id_utilisateur=1,
            sport=self.sport_test,
            date_activite=date(2025, 1, 15),
            distance=0.0,
            duree=timedelta(seconds=2000)
        )
        self.assertNotEqual(activite.calculer_vitesse(), 1.0)  # KO attendu
