import os
import pytest
from unittest.mock import patch
from utils.reset_database import ResetDatabase

from dao.commentaire_dao import CommentaireDao

from business_object.commentaire import Commentaire


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Initialisation des données de test"""
    with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
        ResetDatabase().lancer(test_dao=True)
        yield


def test_creer_ok():
    """Création de Commentaire réussie"""

    # GIVEN
    commentaire = Commentaire(id_activite=991, id_auteur=992, contenu='Super activité !', date_commentaire='2025-09-26')

    # WHEN
    res = CommentaireDao().creer(commentaire)

    # THEN
    assert res
    assert commentaire.id_commentaire


def test_creer_ko():
    """Création de Commentaire échouée (id_activite, id_auteur, contenu et date_commentaire incorrects)"""

    # GIVEN
    commentaire = Commentaire(id_activite='z', id_auteur='a', contenu=5871, date_commentaire='t')

    # WHEN / THEN
    with pytest.raises(Exception):
        res = CommentaireDao().creer(commentaire)

def test_lister_par_activite():
    """Vérifie que la méthode renvoie une liste de Commentaire
    de taille supérieure ou égale à 2
    """
    # GIVEN
    id_ad = 991

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
    id_commentaire = 991

    # WHEN
    suppression_ok = CommentaireDao().supprimer(id_commentaire)

    # THEN
    assert suppression_ok

def test_supprimer_ko():
    """Suppression de commentaire échouée (id inexistant)"""

    # GIVEN
    id_commentaire = 9999

    # WHEN / THEN
    with pytest.raises(Exception):
        suppression_ok = CommentaireDao().supprimer(id_commentaire)

def test_trouver_par_id_ko():
    """Trouver un commentaire inexistant via l'id_activite"""
    # GIVEN
    id_commentaire = 99999

    # WHEN
    commentaire = CommentaireDao().trouver_par_id(id_commentaire)

    # THEN
    assert commentaire is None

def test_trouver_par_id_ok():
    """Trouver un commentaire existant par son id"""
    # GIVEN
    id_commentaire = 992

    # WHEN
    commentaire = CommentaireDao().trouver_par_id(id_commentaire)

    # THEN
    assert commentaire is not None
    assert commentaire.id_commentaire == id_commentaire


if __name__ == "__main__":
    pytest.main([__file__])
