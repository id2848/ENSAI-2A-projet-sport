from datetime import datetime

def verifier_date(date: str) -> bool:
    """Vérifie que la date est au format YYYY-MM-DD"""
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False
