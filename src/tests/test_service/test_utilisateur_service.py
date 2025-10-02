from service.utilisateur_service import UtilisateurService

def test_placeholder():
    """Test temporaire pour garder la pipeline verte
    A supprimer quand de vrais tests seront créés"""

    rep = UtilisateurService().placeholder()

    assert rep is True
