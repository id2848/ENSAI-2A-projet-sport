import pytest

from datetime import date
from business_object.utilisateur import Utilisateur


def test_age_utilisateur():
    """Test le calcul de l'âge de l'utilisateur"""

    # GIVEN
    today = date.today()
    birthdate = date(today.year - 25, today.month, today.day).strftime(
        "%Y-%m-%d"
    )  # 25 ans
    u = Utilisateur(
        pseudo="jeandupont",
        nom="Dupont",
        prenom="Jean",
        date_de_naissance=birthdate,
        sexe="homme",
    )

    # WHEN
    age = u.calculer_age()

    # THEN
    assert age == 25


# Test des validations
def test_valider_pseudo_ok():
    """Test pour la validation du pseudo - valide"""

    # GIVEN
    pseudo_valide = "valid123"

    # WHEN
    res = Utilisateur.valider_pseudo(pseudo_valide)

    # THEN
    assert res


def test_valider_pseudo_ko():
    """Test pour la validation du pseudo - invalide"""

    # GIVEN
    pseudo_invalide = "in"  # Trop court

    # WHEN / THEN
    with pytest.raises(Exception):
        Utilisateur.valider_pseudo(pseudo_invalide)


def test_valider_nom_prenom_ok():
    """Test pour la validation du nom et prénom - valide"""

    # GIVEN
    nom_valide = "Doe"
    prenom_valide = "John"

    # WHEN
    res = Utilisateur.valider_nom_prenom(nom_valide, prenom_valide)

    # THEN
    assert res


def test_valider_nom_prenom_ko():
    """Test pour la validation du nom et prénom - invalide"""

    # GIVEN
    nom_invalide = "Doe123"
    prenom_invalide = "John@"

    # WHEN / THEN
    with pytest.raises(Exception):
        Utilisateur.valider_nom_prenom(nom_invalide, prenom_invalide)


def test_valider_date_naissance_ok():
    """Test pour la validation de la date de naissance - valide"""

    # GIVEN
    date_valide = "1990-01-01"

    # WHEN
    res = Utilisateur.valider_date_naissance(date_valide)

    # THEN
    assert res


def test_valider_date_naissance_ko():
    """Test pour la validation de la date de naissance - invalide"""

    # GIVEN
    date_invalide = "01-01-1990"  # Mauvais format

    # WHEN / THEN
    with pytest.raises(Exception):
        Utilisateur.valider_date_naissance(date_invalide)


def test_valider_sexe_ok():
    """Test pour la validation du sexe - valide"""

    # GIVEN
    sexe_valide = "Femme"

    # WHEN
    res = Utilisateur.valider_sexe(sexe_valide)

    # THEN
    assert res


def test_valider_sexe_ko():
    """Test pour la validation du sexe - invalide"""

    # GIVEN
    sexe_invalide = 5  # Mauvais format

    # WHEN / THEN
    with pytest.raises(Exception):
        Utilisateur.valider_sexe(sexe_invalide)


if __name__ == "__main__":
    pytest.main([__file__])
