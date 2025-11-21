import pytest
from business_object.abonnement import Abonnement


def test_str():
    """Test de la méthode __str__ pour vérifier la représentation lisible de l'objet"""
    abonnement = Abonnement(id_utilisateur_suiveur=1, id_utilisateur_suivi=2)
    expected_str = "Abonnement: Utilisateur 1 suit l'utilisateur 2"
    assert(str(abonnement)== expected_str)

if __name__ == "__main__":
    pytest.main([__file__])
