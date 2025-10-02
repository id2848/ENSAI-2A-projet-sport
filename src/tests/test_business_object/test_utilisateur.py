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
        mot_de_passe_hash="hash",
        nom="Dupont",
        prenom="Jean",
        date_de_naissance=birthdate,
        sexe="M"
    )

    # WHEN
    age = u.age()

    # THEN
    assert u.age() == 25
