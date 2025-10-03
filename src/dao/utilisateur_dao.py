from typing import List, Optional
from business_object.utilisateur import Utilisateur
from business_object.activite import Activite
from business_object.commentaire import Commentaire
from business_object.jaime import Jaime
from business_object.abonnement import Abonnement

class UtilisateurDAO:
    def get(id: str) -> Utilisateur:
        pass