import os
import pytest
from unittest.mock import patch
from utils.reset_database import ResetDatabase

from datetime import date, timedelta

from service.activite_service import ActiviteService

from business_object.activite import Activite
from business_object.jaime import Jaime
from business_object.commentaire import Commentaire
from business_object.utilisateur import Utilisateur

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
    sport = 'course'
    date_activite = date(2025, 9, 25)  # Date d'activité existante
    distance = 5.0
    duree = 30.0

    # WHEN
    activite = ActiviteService().creer_activite(id_utilisateur, sport, date_activite, distance, duree)

    # THEN
    # Vérifie que l'activité est créée correctement
    assert activite is True

def test_creer_activite_echec():
    """Test pour la création d'une activité échouée (par exemple, si l'utilisateur n'existe pas)"""

    # GIVEN
    id_utilisateur = 99999999  # Un utilisateur qui n'existe pas
    sport = 'course'
    date_activite = date(2025, 9, 25)
    distance = 5.0
    duree = 30.0

    # WHEN
    activite = ActiviteService().creer_activite(id_utilisateur, sport, date_activite, distance, duree)

    # THEN
    assert activite is False

def test_lister_activites():
    """Test pour lister les activités d'un utilisateur"""
    
    # GIVEN
    id_utilisateur = 992

    # WHEN
    activites = ActiviteService().lister_activites(id_utilisateur)

    # THEN
    assert len(activites) == 1  # Vérifier qu'il y a 1 activité pour l'utilisateur 992
    assert activites[0].id_activite == 992  # Vérifier que l'activité retournée est celle de l'utilisateur 992
    assert activites[0].sport == 'natation'  # Vérifier que le sport de l'activité est "natation"
    assert activites[0].date_activite == date(2025, 9, 26)  # Vérifier que la date de l'activité est correcte
    assert activites[0].distance == 2.5  # Vérifier la distance de l'activité
    assert activites[0].duree == 45.0  # Vérifier la durée de l'activité

def test_lister_activites_filtres_sport():
    """Test pour lister les activités d'un utilisateur filtrées par sport"""

    # GIVEN
    id_utilisateur = 992
    sport_filtree = 'course'  # On cherche des activités de sport "course"

    # WHEN
    activites = ActiviteService().lister_activites_filtres(id_utilisateur, sport=sport_filtree)

    # THEN
    assert len(activites) == 0  # Aucun résultat car l'utilisateur 992 n'a pas d'activité "course"

def test_lister_activites_filtres_date():
    """Test pour lister les activités d'un utilisateur filtrées par plage de dates"""
    
    # GIVEN
    id_utilisateur = 993
    date_debut = '2025-09-25'
    date_fin = '2025-09-28'

    # WHEN
    activites = ActiviteService().lister_activites_filtres(id_utilisateur, date_debut=date_debut, date_fin=date_fin)

    # THEN
    assert len(activites) == 1  # Il y a une activité pour "samsmith" dans cette plage de dates (le 2025-09-27)
    assert activites[0].id_activite == 993  # Vérifier que l'activité correspond à celle de "samsmith"
    assert activites[0].sport == 'vélo'  # Vérifier que le sport de l'activité est "vélo"
    assert activites[0].date_activite == date(2025, 9, 27)  # Vérifier la date de l'activité

def test_lister_activites_filtres_sport_et_date():
    """Test pour lister les activités d'un utilisateur filtrées par sport et dates"""
    
    # GIVEN
    id_utilisateur = 992
    sport_filtree = 'natation'
    date_debut = '2025-09-25'
    date_fin = '2025-09-28'

    # WHEN
    activites = ActiviteService().lister_activites_filtres(id_utilisateur, sport=sport_filtree, date_debut=date_debut, date_fin=date_fin)

    # THEN
    assert len(activites) == 1  # Une seule activité de sport "natation" pour "janedoe" dans cette plage de dates
    assert activites[0].id_activite == 992  # Vérifier que l'activité correspond à celle de "janedoe"
    assert activites[0].sport == 'natation'  # Vérifier que le sport de l'activité est "natation"
    assert activites[0].date_activite == date(2025, 9, 26)  # Vérifier la date de l'activité
    assert activites[0].distance == 2.5  # Vérifier la distance de l'activité
    assert activites[0].duree == 45.0  # Vérifier la durée de l'activité

def test_trouver_activite_par_id_ko():
    """Trouver une activité inexistante via l'id_activite"""
    # GIVEN
    id_activite = 99999

    # WHEN
    activite = ActiviteService().trouver_activite_par_id(id_activite)

    # THEN
    assert activite is None


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
    result = ActiviteService().ajouter_jaime(id_activite, id_utilisateur)

    # THEN
    assert result is True

def test_ajouter_jaime_echec():
    """Test pour l'échec de l'ajout d'un 'j'aime' (par exemple, si l'activité n'existe pas)"""

    # GIVEN
    id_utilisateur = 99999  # Un utilisateur qui n'existe pas
    id_activite = 999  # Une activité qui n'existe pas

    # WHEN
    result = ActiviteService().ajouter_jaime(id_activite, id_utilisateur)

    # THEN
    assert result is False

def test_lister_commentaires():
    """Test pour lister les commentaires d'une activité"""

    # GIVEN
    id_activite = 993  # Activité de Sam Smith

    # WHEN
    commentaires = ActiviteService().lister_commentaires(id_activite)

    # THEN
    assert len(commentaires) == 1
    assert commentaires[0].commentaire == "J'adore le vélo !"  # Le commentaire de Sam

def test_ajouter_commentaire_ok():
    """Test pour ajouter un commentaire à une activité"""

    # GIVEN
    id_utilisateur = 991  # John Doe
    id_activite = 994  # Activité de Emily Jones
    commentaire = "Très belle randonnée !"

    # WHEN
    result = ActiviteService().ajouter_commentaire(id_utilisateur, id_activite, commentaire)

    # THEN
    assert result is True

def test_ajouter_commentaire_echec():
    """Test pour l'échec de l'ajout d'un commentaire (par exemple, si l'activité n'existe pas)"""

    # GIVEN
    id_utilisateur = 999  # Un utilisateur qui n'existe pas
    id_activite = 999  # Une activité qui n'existe pas
    commentaire = "Super activité !"

    # WHEN
    result = ActiviteService().ajouter_commentaire(id_utilisateur, id_activite, commentaire)

    # THEN
    assert result is False

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

    # WHEN
    result = ActiviteService().supprimer_activite(id_activite)

    # THEN
    assert result is False

def test_trouver_commentaire_par_id_ko():
    """Trouver un commentaire inexistant via l'id_activite"""
    # GIVEN
    id_commentaire = 99999

    # WHEN
    commentaire = ActiviteService().trouver_commentaire_par_id(id_commentaire)

    # THEN
    assert commentaire is None

def test_trouver_commentaire_par_id_ok():
    """Trouver un commentaire existant par son id"""
    # GIVEN
    id_commentaire = 992

    # WHEN
    commentaire = ActiviteService().trouver_commentaire_par_id(id_commentaire)

    # THEN
    assert commentaire is not None
    assert commentaire.id_commentaire == id_commentaire

if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
