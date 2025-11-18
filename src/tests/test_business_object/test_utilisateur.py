from datetime import date
from business_object.utilisateur import Utilisateur


def test_age_utilisateur():
    """Test le calcul de l'âge de l'utilisateur"""
    
    # GIVEN
    today = date.today()
    birthdate = date(today.year - 25, today.month, today.day)  # 25 ans
    u = Utilisateur(
        id_utilisateur=1,
        pseudo="jean_dupont",
        nom="Dupont",
        prenom="Jean",
        date_de_naissance=birthdate,
        sexe="M"
    )

    # WHEN
    age = u.calculer_age()

    # THEN
    assert age == 25

# Test des validations
def test_valider_pseudo():
    """Test pour la validation du pseudo"""

    # GIVEN
    pseudo_valide = "valid123"
    pseudo_invalide = "in"  # Trop court

    # WHEN
    validation_valide = Utilisateur.valider_pseudo(pseudo_valide)
    validation_invalide = Utilisateur.valider_pseudo(pseudo_invalide)

    # THEN
    assert validation_valide is True  # Le pseudo valide doit être accepté
    assert validation_invalide is False  # Le pseudo invalide doit être rejeté

def test_valider_nom_prenom():
    """Test pour la validation du nom et prénom"""

    # GIVEN
    nom_valide = "Doe"
    prenom_valide = "John"
    nom_invalide = "Doe123"
    prenom_invalide = "John@"

    # WHEN
    validation_valide = Utilisateur.valider_nom_prenom(nom_valide, prenom_valide)
    validation_invalide = Utilisateur.valider_nom_prenom(nom_invalide, prenom_invalide)

    # THEN
    assert validation_valide is True  # Nom et prénom valides
    assert validation_invalide is False  # Nom et prénom invalides


def test_valider_date_naissance():
    """Test pour la validation de la date de naissance"""

    # GIVEN
    date_valide = "1990-01-01"
    date_invalide = "01-01-1990"  # Mauvais format

    # WHEN
    validation_valide = Utilisateur.valider_date_naissance(date_valide)
    validation_invalide = Utilisateur.valider_date_naissance(date_invalide)

    # THEN
    assert validation_valide is True  # La date doit être valide
    assert validation_invalide is False  # La date doit être invalide


def test_valider_sexe():
    """Test pour la validation du sexe"""

    # GIVEN
    sexe_valide = "homme"
    sexe_invalide = "invalide"  # Sexe non reconnu

    # WHEN
    validation_valide = Utilisateur.valider_sexe(sexe_valide)
    validation_invalide = Utilisateur.valider_sexe(sexe_invalide)

    # THEN
    assert validation_valide is True  # Sexe valide
    assert validation_invalide is False  # Sexe invalide
