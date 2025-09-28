import hashlib
import os,shutil
from uuid import UUID
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.encryption_services import encryption_service
from app.models.media import Media
from app.schemas.media import MediaCreate

def save_temp_file(
    *,
    db: Session, 
    temp_file: MediaCreate, 
    file: UploadFile,
    file_type: str
):
    
    temp_media = Media(**temp_file.model_dump())
    db.add(temp_media)
    db.commit()
    db.refresh(temp_media)
    
    
    # créer un dossier temporaire pour les fichiers
    temp_dir = "/tmp/uploads"
    os.makedirs(temp_dir, exist_ok=True)
    
    # chemin de fichier temporaire
    temp_path = f"{temp_dir}/{temp_media.id}_{file.filename}"
    
    # copier le fichier en memoire sur le disque
    with open(temp_path, "wb") as temp_file_handle:
        shutil.copyfileobj(file.file, temp_file_handle)

    return temp_path, temp_media

def calculate_file_checksum(file_path: str) -> str:
    """Calcule le checksum SHA-256 d'un fichier"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Lire par chunks pour les gros fichiers
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

# n'est pas encore utilisé
def update_missing_media_fields(db: Session, media_id: UUID):
    """Met à jour les champs manquants pour un média existant"""
    media = db.query(Media).filter(Media.id == media_id).first()
    if not media or not media.file_path:
        return None
    
    try:
        # Si le fichier est encrypté, on ne peut pas calculer sa taille originale
        # mais on peut avoir la taille du fichier encrypté
        encrypted_file_size = os.path.getsize(media.file_path)
        
        # Mise à jour des champs
        if not media.file_size:
            # Pour un fichier encrypté, on estime la taille originale
            # (Fernet ajoute environ 60 bytes d'overhead + base64 encoding)
            estimated_original_size = int((encrypted_file_size - 60) * 0.75)
            media.file_size = estimated_original_size
        
        if not media.encryption_key_id:
            media.encryption_key_id = "default_key_v1"
            
        if not media.storage_location:
            media.storage_location = "local"
            
        if not media.checksum:
            # Pour un fichier encrypté, on calcule le checksum du fichier encrypté
            media.checksum = calculate_file_checksum(media.file_path)
        
        db.commit()
        return media
        
    except Exception as e:
        print(f"Erreur lors de la mise à jour du média {media_id}: {e}")
        return None
    