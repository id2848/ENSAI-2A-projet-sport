class DatabaseCreationError(Exception):
    """Levé lors de l'échec d'une création dans la base de données"""
    pass

class DatabaseDeletionError(Exception):
    """Levé lors de l'échec d'une suppression dans la base de données"""
    pass

class DatabaseUpdateError(Exception):
    """Levé lors de l'échec d'une modification dans la base de données"""
    pass

class UserNotFoundError(Exception):
    """Levé lorsqu'un utilisateur n'existe pas"""
    pass

class InvalidPasswordError(Exception):
    """Levé lorsque le mot de passe ne correspond pas à un utilisateur"""
