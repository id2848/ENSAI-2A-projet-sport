import unittest
from datetime import timedelta, date
from business_object.activite import Activite
from service.service_statistiques import ServiceStatistiques


class ActiviteDaoMock:
    def __init__(self, activites=None):
        self._activites = activites or []

    def lister_par_utilisateur(self, id_utilisateur):
        return [a for a in self._activites if a.id_utilisateur == id_utilisateur]


class TestServiceStatistiques(unittest.TestCase):
    """Tests unitaires pour ServiceStatistiques (mode OK/KO)"""

    def setUp(self):
        """Préparation des données avant chaque test"""
        self.sport = "Course"
        self.activites = [
            Activite(id_activite=1, id_utilisateur=1, sport=self.sport, date_activite=date(2025,1,1), distance=5.0, duree=timedelta(minutes=30)),
            Activite(id_activite=2, id_utilisateur=1, sport=self.sport, date_activite=date(2025,1,2), distance=10.0, duree=timedelta(hours=1)),
            Activite(id_activite=3, id_utilisateur=2, sport=self.sport, date_activite=date(2025,1,3), distance=7.0, duree=timedelta(minutes=45))
        ]
        self.service = ServiceStatistiques()
        self.service.activite_dao = ActiviteDaoMock(self.activites)

    def test_calculer_nombre_activites_ok(self):
        self.assertEqual(self.service.calculer_nombre_activites(1), 2)
        self.assertEqual(self.service.calculer_nombre_activites(2), 1)

    def test_calculer_distance_totale_ok(self):
        self.assertEqual(self.service.calculer_distance_totale(1), 15.0)
        self.assertEqual(self.service.calculer_distance_totale(2), 7.0)

    def test_calculer_duree_totale_ok(self):
        total_sec_user1 = 30*60 + 60*60 
        self.assertEqual(self.service.calculer_duree_totale(1), total_sec_user1)
        self.assertEqual(self.service.calculer_duree_totale(2), total_sec_user2)

    def test_calculer_nombre_activites_ko(self):
        # Utilisateur sans activité
        self.assertEqual(self.service.calculer_nombre_activites(99), 0)

    def test_calculer_distance_totale_ko(self):
        # Utilisateur sans activité → distance totale = 0.0
        self.assertEqual(self.service.calculer_distance_totale(99), 0.0)

    def test_calculer_duree_totale_ko(self):
        # Utilisateur sans activité → durée totale = 0
        self.assertEqual(self.service.calculer_duree_totale(99), 0)


if __name__ == "__main__":
    unittest.main()
