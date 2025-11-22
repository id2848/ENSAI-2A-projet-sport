import os
import pytest
from unittest.mock import patch
from utils.reset_database import ResetDatabase

from datetime import date

from service.activite_service import ActiviteService


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Initialisation des données de test dans la base de données"""
    # Assurez-vous d'utiliser un schéma de test pour éviter de modifier la vraie base de données
    with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
        # Reset de la base de données avant de commencer
        ResetDatabase().lancer(test_dao=True)
        yield


def test_creer_activite_ok():
    """Test pour la création d'une activité réussie"""

    # GIVEN
    id_utilisateur = 991  # John Doe
    sport = "course"
    date_activite = "2025-09-30"
    distance = 5.0
    duree = 30.0

    # WHEN
    activite = ActiviteService().creer_activite(
        id_utilisateur, sport, date_activite, distance, duree
    )

    # THEN
    # Vérifie que l'activité est créée correctement
    assert activite


def test_creer_activite_echec():
    """Test pour la création d'une activité échouée (par exemple, si l'utilisateur n'existe pas)"""

    # GIVEN
    id_utilisateur = 99999999  # Un utilisateur qui n'existe pas
    sport = "course"
    date_activite = date(2025, 9, 25)
    distance = 5.0
    duree = 30.0

    # WHEN / THEN
    with pytest.raises(Exception):
        ActiviteService().creer_activite(
            id_utilisateur, sport, date_activite, distance, duree
        )


def test_lister_activites():
    """Test pour lister les activités d'un utilisateur"""

    # GIVEN
    id_utilisateur = 992

    # WHEN
    activites = ActiviteService().lister_activites(id_utilisateur)

    # THEN
    assert len(activites) == 1  # Vérifier qu'il y a 1 activité pour l'utilisateur 992
    assert (
        activites[0].id_activite == 992
    )  # Vérifier que l'activité retournée est celle de l'utilisateur 992
    assert (
        activites[0].sport == "natation"
    )  # Vérifier que le sport de l'activité est "natation"
    assert activites[0].date_activite == date(
        2025, 9, 26
    )  # Vérifier que la date de l'activité est correcte
    assert activites[0].distance == 2.5  # Vérifier la distance de l'activité
    assert activites[0].duree == 45.0  # Vérifier la durée de l'activité


def test_lister_activites_filtres_sport():
    """Test pour lister les activités d'un utilisateur filtrées par sport"""

    # GIVEN
    id_utilisateur = 992
    sport_filtree = "course"  # On cherche des activités de sport "course"

    # WHEN
    activites = ActiviteService().lister_activites_filtres(
        id_utilisateur, sport=sport_filtree
    )

    # THEN
    assert (
        len(activites) == 0
    )  # Aucun résultat car l'utilisateur 992 n'a pas d'activité "course"


def test_lister_activites_filtres_date():
    """Test pour lister les activités d'un utilisateur filtrées par plage de dates"""

    # GIVEN
    id_utilisateur = 993
    date_debut = "2025-09-25"
    date_fin = "2025-09-28"

    # WHEN
    activites = ActiviteService().lister_activites_filtres(
        id_utilisateur, date_debut=date_debut, date_fin=date_fin
    )

    # THEN
    assert (
        len(activites) == 1
    )  # Il y a une activité pour "samsmith" dans cette plage de dates (le 2025-09-27)
    assert (
        activites[0].id_activite == 993
    )  # Vérifier que l'activité correspond à celle de "samsmith"
    assert (
        activites[0].sport == "vélo"
    )  # Vérifier que le sport de l'activité est "vélo"
    assert activites[0].date_activite == date(
        2025, 9, 27
    )  # Vérifier la date de l'activité


def test_lister_activites_filtres_sport_et_date():
    """Test pour lister les activités d'un utilisateur filtrées par sport et dates"""

    # GIVEN
    id_utilisateur = 992
    sport_filtree = "natation"
    date_debut = "2025-09-25"
    date_fin = "2025-09-28"

    # WHEN
    activites = ActiviteService().lister_activites_filtres(
        id_utilisateur, sport=sport_filtree, date_debut=date_debut, date_fin=date_fin
    )

    # THEN
    assert (
        len(activites) == 1
    )  # Une seule activité de sport "natation" pour "janedoe" dans cette plage de dates
    assert (
        activites[0].id_activite == 992
    )  # Vérifier que l'activité correspond à celle de "janedoe"
    assert (
        activites[0].sport == "natation"
    )  # Vérifier que le sport de l'activité est "natation"
    assert activites[0].date_activite == date(
        2025, 9, 26
    )  # Vérifier la date de l'activité
    assert activites[0].distance == 2.5  # Vérifier la distance de l'activité
    assert activites[0].duree == 45.0  # Vérifier la durée de l'activité


def test_trouver_activite_par_id_ko():
    """Trouver une activité inexistante via l'id_activite"""
    # GIVEN
    id_activite = 99999

    # WHEN / THEN
    with pytest.raises(Exception):
        ActiviteService().trouver_activite_par_id(id_activite)


def test_trouver_activite_par_id_ok():
    """Trouver une activité existante par son id"""
    # GIVEN
    id_activite = 991

    # WHEN
    activite = ActiviteService().trouver_activite_par_id(id_activite)

    # THEN
    assert activite is not None
    assert activite.id_activite == id_activite


def test_ajouter_jaime_ok():
    """Test pour l'ajout d'un 'j'aime' à une activité"""

    # GIVEN
    id_activite = 993
    id_utilisateur = 992

    # WHEN
    res = ActiviteService().ajouter_jaime(id_activite, id_utilisateur)

    # THEN
    assert res


def test_ajouter_jaime_echec():
    """Test pour l'échec de l'ajout d'un 'j'aime' (par exemple, si l'activité n'existe pas)"""

    # GIVEN
    id_utilisateur = 99999  # Un utilisateur qui n'existe pas
    id_activite = 999  # Une activité qui n'existe pas

    # WHEN / THEN
    with pytest.raises(Exception):
        ActiviteService().ajouter_jaime(id_activite, id_utilisateur)


def test_supprimer_jaime_ok():
    """Suppression d'un jaime réussie"""

    # GIVEN
    id_activite = 993
    id_auteur = 991

    # WHEN
    suppression_ok = ActiviteService().supprimer_jaime(id_activite, id_auteur)

    # THEN
    assert suppression_ok


def test_supprimer_jaime_ko():
    """Suppression d'un jaime échouée (jaime inexistant)"""

    # GIVEN
    id_activite = 991
    id_auteur = 995

    # WHEN / THEN
    with pytest.raises(Exception):
        ActiviteService().supprimer_jaime(id_activite, id_auteur)


def test_lister_commentaires():
    """Test pour lister les commentaires d'une activité"""

    # GIVEN
    id_activite = 993  # Activité de Sam Smith

    # WHEN
    commentaires = ActiviteService().lister_commentaires(id_activite)

    # THEN
    assert len(commentaires) == 1
    assert commentaires[0].contenu == "J'adore le vélo !"  # Le commentaire de Sam


def test_ajouter_commentaire_ok():
    """Test pour ajouter un commentaire à une activité"""

    # GIVEN
    id_activite = 994  # Activité de Emily Jones
    id_utilisateur = 991  # John Doe
    contenu = "Très belle randonnée !"

    # WHEN
    res = ActiviteService().ajouter_commentaire(id_activite, id_utilisateur, contenu)

    # THEN
    assert res


def test_ajouter_commentaire_echec():
    """Test pour l'échec de l'ajout d'un commentaire (par exemple, si l'activité n'existe pas)"""

    # GIVEN
    id_activite = 9999  # Une activité qui n'existe pas
    id_utilisateur = 991
    contenu = "Super activité !"

    # WHEN / THEN
    with pytest.raises(Exception):
        ActiviteService().ajouter_commentaire(id_activite, id_utilisateur, contenu)


def test_supprimer_commentaire_ok():
    """Suppression de commentaire réussie"""

    # GIVEN
    id_commentaire = 991

    # WHEN
    suppression_ok = ActiviteService().supprimer_commentaire(id_commentaire)

    # THEN
    assert suppression_ok


def test_supprimer_commentaire_ko():
    """Suppression de commentaire échouée (id inexistant)"""

    # GIVEN
    id_commentaire = 9999

    # WHEN / THEN
    with pytest.raises(Exception):
        ActiviteService().supprimer_commentaire(id_commentaire)


def test_supprimer_activite_ok():
    """Test pour la suppression d'une activité"""

    # GIVEN
    id_activite = 991  # L'activité de John Doe

    # WHEN
    result = ActiviteService().supprimer_activite(id_activite)

    # THEN
    assert result is True


def test_supprimer_activite_echec():
    """Test pour l'échec de la suppression d'une activité (par exemple, si l'activité n'existe pas)"""

    # GIVEN
    id_activite = 9999  # Une activité qui n'existe pas

    # WHEN / THEN
    with pytest.raises(Exception):
        ActiviteService().supprimer_activite(id_activite)


def test_trouver_commentaire_par_id_ko():
    """Trouver un commentaire inexistant via l'id_activite"""
    # GIVEN
    id_commentaire = 99999

    # WHEN / THEN
    with pytest.raises(Exception):
        ActiviteService().trouver_commentaire_par_id(id_commentaire)


def test_trouver_commentaire_par_id_ok():
    """Trouver un commentaire existant par son id"""
    # GIVEN
    id_commentaire = 992

    # WHEN
    commentaire = ActiviteService().trouver_commentaire_par_id(id_commentaire)

    # THEN
    assert commentaire is not None
    assert commentaire.id_commentaire == id_commentaire


def test_jaime_existe_ok():
    """Vérifier qu'un jaime existe pour une activité et un utilisateur donnés"""

    # GIVEN
    id_activite = 991
    id_utilisateur = 993

    # WHEN
    existe = ActiviteService().jaime_existe(
        id_activite=id_activite, id_utilisateur=id_utilisateur
    )

    # THEN
    assert existe


def test_jaime_existe_ko():
    """Vérifier qu'un jaime n'existe pas"""

    # GIVEN
    id_activite = 991
    id_utilisateur = 995

    # WHEN
    existe = ActiviteService().jaime_existe(
        id_activite=id_activite, id_utilisateur=id_utilisateur
    )

    # THEN
    assert not existe


def test_compter_jaimes_par_activite_existante():
    """Compter le nombre de jaimes pour une activité existante"""
    # GIVEN
    id_activite = 991  # présent dans les données de test

    # WHEN
    count = ActiviteService().compter_jaimes_par_activite(id_activite)

    # THEN
    assert isinstance(count, int)
    assert count == 1  # d'après les données test


def test_compter_jaimes_par_activite_inexistante():
    """Compter le nombre de jaimes pour une activité inexistante"""
    # GIVEN
    id_activite = 99999  # inexistant

    # WHEN / THEN
    with pytest.raises(Exception):
        ActiviteService().compter_jaimes_par_activite(id_activite)


if __name__ == "__main__":
    pytest.main([__file__])
