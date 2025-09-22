import os
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.media import Media
from app.encryption_services import encryption_service
from app.utils.media import calculate_file_checksum

async def encrypt_and_store(
    db: Session, 
    media_id: UUID, 
    temp_path: str, 
    file_type: str,
):
    try:
       
        file_size = os.path.getsize(temp_path)
        checksum = calculate_file_checksum(temp_path)
        
        
        encrypted_path = encryption_service.encrypt_and_move_file(
            temp_path, 
            str(media_id), 
            file_type
        )
        
        print("3: ", encrypted_path)
        
        
        media = db.query(Media).filter(Media.id == media_id).first()
        if media:
            media.file_path = encrypted_path
            media.file_size = file_size
            media.checksum = checksum
            media.encryption_key_id = "default_key_v1" 
            media.storage_location = "local"
            media.status = "processed"
            
            db.commit()
            
            print(f"Média {media_id} traité avec succès")
        
    except Exception as e:
        
        media = db.query(Media).filter(Media.id == media_id).first()
        if media:
            media.status = "error"
            db.commit()
        
        
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        print(f"Erreur lors du traitement du média {media_id}: {e}")


