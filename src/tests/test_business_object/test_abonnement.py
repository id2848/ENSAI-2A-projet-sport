import unittest
from business_object.abonnement import Abonnement

class TestAbonnement(unittest.TestCase):
    
    def setUp(self):
        """Préparation des objets nécessaires pour les tests"""
        # Création d'un abonnement pour les tests
        self.abonnement = Abonnement(id_utilisateur_suiveur=1, id_utilisateur_suivi=2)
    
    def test_initialisation(self):
        """Vérifie si l'initialisation de l'abonnement est correcte"""
        self.assertEqual(self.abonnement.get_id_utilisateur_suiveur(), 1)
        self.assertEqual(self.abonnement.get_id_utilisateur_suivi(), 2)
    
    def test_get_id_utilisateur_suiveur(self):
        """Test pour récupérer l'ID du suiveur"""
        self.assertEqual(self.abonnement.get_id_utilisateur_suiveur(), 1)
    
    def test_get_id_utilisateur_suivi(self):
        """Test pour récupérer l'ID du suivi"""
        self.assertEqual(self.abonnement.get_id_utilisateur_suivi(), 2)
    
    def test_str(self):
        """Test de la méthode __str__ pour vérifier la représentation lisible de l'objet"""
        expected_str = "Abonnement: Utilisateur 1 suit l'utilisateur 2"
        self.assertEqual(str(self.abonnement), expected_str)

if __name__ == "__main__":
    unittest.main()
