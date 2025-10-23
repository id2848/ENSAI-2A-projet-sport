import os
import pytest
import unittest

from unittest.mock import patch

from utils.reset_database import ResetDatabase
from utils.securite import hash_password
from business_object.abonnement import Abonnement
from dao.abonnement_dao import AbonnementDao


class TestAbonnement(unittest.TestCase):
    
    def setUp(self):
        """Préparation des données pour les tests."""
        self.abonnement = Abonnement(id_utilisateur_suiveur=1, id_utilisateur_suivi=2)

    def test_get_id_utilisateur_suiveur(self):
        """Test que l'ID de l'utilisateur suiveur est correct."""
        self.assertEqual(self.abonnement.get_id_utilisateur_suiveur(), 1)

    def test_get_id_utilisateur_suivi(self):
        """Test que l'ID de l'utilisateur suivi est correct."""
        self.assertEqual(self.abonnement.get_id_utilisateur_suivi(), 2)

    def test_egalite_abonnement(self):
        """Test que deux abonnements avec les mêmes utilisateurs sont égaux."""
        abonnement_2 = Abonnement(id_utilisateur_suiveur=1, id_utilisateur_suivi=2)
        self.assertEqual(self.abonnement.get_id_utilisateur_suiveur(), abonnement_2.get_id_utilisateur_suiveur())
        self.assertEqual(self.abonnement.get_id_utilisateur_suivi(), abonnement_2.get_id_utilisateur_suivi())

    def test_inegalite_abonnement(self):
        """Test que deux abonnements avec des utilisateurs différents ne sont pas égaux."""
        abonnement_3 = Abonnement(id_utilisateur_suiveur=3, id_utilisateur_suivi=4)
        self.assertNotEqual(self.abonnement.get_id_utilisateur_suiveur(), abonnement_3.get_id_utilisateur_suiveur())
        self.assertNotEqual(self.abonnement.get_id_utilisateur_suivi(), abonnement_3.get_id_utilisateur_suivi())

# Lancer les tests
if __name__ == "__main__":
    unittest.main()
