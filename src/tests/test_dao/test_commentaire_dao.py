import os
import pytest

from unittest.mock import patch

from utils.reset_database import ResetDatabase
from utils.securite import hash_password

from dao.commentaire_dao import CommentaireDao

from business_object.commentaire import Commentaire


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialisation des données de test"""
    with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
        ResetDatabase().lancer(test_dao=True)
        yield


def test_creer_ok():
    """Création de Commentaire réussie"""

    # GIVEN
    commentaire = Commentaire(id_activite=991, id_auteur=992, commentaire="ok !", date_commentaire=2025-10-21)

    # WHEN
    creation_ok = CommentaireDao().creer(commentaire)

    # THEN
    assert creation_ok
    assert commentaire.id_commentaire


def test_creer_ko():
    """Création de Joueur échouée (id_activite, id_auteur, commentaire et date_commentaire incorrects)"""

    # GIVEN
    commentaire = Commentaire(id_activite='z', id_auteur='a', commentaire=5871, date_commentaire='t')

    # WHEN
    creation_ok = CommentaireDao().creer(commentaire)

    # THEN
    assert not creation_ok

def test_lister_par_activite():
    """Vérifie que la méthode renvoie une liste de Joueur
    de taille supérieure ou égale à 2
    """
    # GIVEN
    id_ad =991

    # WHEN
    commentaires = CommentaireDao().lister_par_activite(id_activite=id_ad)

    # THEN
    assert isinstance(commentaires, list)
    for j in commentaires:
        assert isinstance(j, Commentaire)
    assert len(commentaires) >= 1

def test_supprimer_ok():
    """Suppression de commentaire réussie"""

    # GIVEN
    commentaire = Commentaire(id_activite=993, id_auteur=994, commentaire='J''adore le vélo !', date_commentaire='2025-09-28')

    # WHEN
    suppression_ok = CommentaireDao().supprimer(commentaire)

    # THEN
    assert suppression_ok


def test_supprimer_ko():
    """Suppression de commentaire échouée (id inconnu)"""

    # GIVEN
    commentaire = Commentaire(id_activite=123, id_auteur=456, commentaire="ok !", date_commentaire=2025-10-21)

    # WHEN
    suppression_ok = CommentaireDao().supprimer(commentaire)

    # THEN
    assert not suppression_ok


if __name__ == "__main__":
    pytest.main([__file__])
