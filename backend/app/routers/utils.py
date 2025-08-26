from fastapi import HTTPException

from backend.app.exc import NotFoundError, DatabaseError, DuplicateError

def handle_app_error(e: Exception):
    """
    Fonction utilitaire pour gérer les erreurs
    """
    if isinstance(e, NotFoundError):
        raise HTTPException(status_code=404, message=e.message)
    if isinstance(e, DuplicateError):
        raise HTTPException(status_code=409, message=e.message)
    if isinstance(e, DatabaseError):
        raise HTTPException(status_code=500, message=e.message)
    else :
        raise HTTPException(status_code=400, detail=str(e))