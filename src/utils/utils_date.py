from datetime import datetime, date


def verifier_date(date: str) -> bool:
    """Vérifie que la date est un str au format YYYY-MM-DD"""
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def valider_date(var_date: date | str) -> date:
    """Valider que la date est une date ou bien un str au format YYYY-MM-DD à convertir
    Renvoie un objet 'date'"""
    if isinstance(var_date, date):
        return var_date
    elif isinstance(var_date, str):
        return datetime.strptime(
            var_date, "%Y-%m-%d"
        ).date()  # lève une ValueError si la date n'est pas au format YYYY-MM-DD
    else:
        raise ValueError("var_date doit être une date ou un str")
