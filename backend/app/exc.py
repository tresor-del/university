
class AppError(Exception):
    """
    Classe de base pour les exceptions personnalisées
    """
    pass

class NotFoundError(AppError):
    """
    Est levé quand une ressource n'est pas trouvé
    """
    def __init__(self, message="Ressource non trouvé"):
        self.message = message
        super().__init__(message)

class DuplicateError(AppError):
    """
    Est levé si on essaie de créer une ressource dupliquée
    """
    def __init__(self, message="La ressource existe déjà"):
        self.message = message
        super().__init__(message)

class DatabaseError(AppError):
    """
    Erreurs de la base de donnée
    """
    def __init__(self, message="Erreur de la base de donné"):
        self.message = message
        super().__init__(message)
