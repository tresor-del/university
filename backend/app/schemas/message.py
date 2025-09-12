from pydantic import BaseModel

class Message(BaseModel):
    """
    Schemas d'envoie de message
    """
    message: str