import hashlib
import os


def generer_salt(taille: int = 16) -> str:
    """Génère un sel aléatoire sous forme hexadécimale."""
    return os.urandom(taille).hex()


def hash_password(password: str, sel: str = "") -> str:
    """Hachage du mot de passe avec SHA-256 et un sel."""
    password_bytes = password.encode("utf-8") + sel.encode("utf-8")
    hash_object = hashlib.sha256(password_bytes)
    return hash_object.hexdigest()


def verifier_mot_de_passe(mot_de_passe_clair: str, sel: str, hash_stocke: str) -> bool:
    """Vérifie si le mot de passe clair correspond au hash stocké."""
    return hash_password(mot_de_passe_clair, sel) == hash_stocke
