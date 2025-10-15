import os
import shutil
from datetime import datetime
from cryptography.fernet import Fernet
from typing import Optional

class FileEncryptionService:
    def __init__(self, base_storage_path: str = "backend/app/encrypted_files"):
        self.base_storage_path = base_storage_path
        self.encryption_key_id = "default_key_v1"  # Version de la clé
        self.encryption_key = self._get_encryption_key()
        self.fernet = Fernet(self.encryption_key)
    
    def _get_encryption_key(self) -> bytes:
        # Récupère ou génère la clé d'encryption
        key_file = f"encryption_{self.encryption_key_id}.key"
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            return key
    
    def get_key_id(self) -> str:
        """Retourne l'ID de la clé d'encryption utilisée"""
        return self.encryption_key_id
    
    def create_storage_path(self, media_id: str, file_type: str) -> str:
        """Crée le chemin de stockage organisé"""
        date_folder = datetime.now().strftime("%Y/%m")
        storage_dir = f"{self.base_storage_path}/{file_type}/{date_folder}"
        
        # Créer les dossiers s'ils n'existent pas
        os.makedirs(storage_dir, exist_ok=True)
        
        return f"{storage_dir}/{media_id}.enc"
    
    def encrypt_and_move_file(self, temp_path: str, media_id: str, file_type: str) -> str:
        """
        Encrypte un fichier temporaire et le déplace vers le stockage final
        
        Les arguments à prendre:
            temp_path: Chemin du fichier temporaire
            media_id: ID du média pour le naming
            file_type: Type de fichier (photo, document, qr_code)
            
        Ce qu'elle retourne:
            str: Chemin du fichier encrypté final
        """
        #  Créer le chemin de destination
        encrypted_path = self.create_storage_path(media_id, file_type)
        
        # Lire le fichier temporaire
        with open(temp_path, 'rb') as temp_file:
            file_data = temp_file.read()
        
        # Encrypter les données
        encrypted_data = self.fernet.encrypt(file_data)
        
        # Sauvegarder le fichier encrypté
        with open(encrypted_path, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)
        
        # Supprimer le fichier temporaire
        os.remove(temp_path)
        
        return encrypted_path
    
    def decrypt_file(self, encrypted_path: str) -> bytes:
        """Décrypte un fichier et retourne les données"""
        with open(encrypted_path, 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()
        
        return self.fernet.decrypt(encrypted_data)
    
    # cette fonction n'est pas encore utilisée
    def decrypt_file_to_temp(self, encrypted_path: str, temp_name: str) -> str:
        """Décrypte un fichier vers un fichier temporaire"""
        decrypted_data = self.decrypt_file(encrypted_path)
        
        temp_dir = "/tmp"  
        temp_path = f"{temp_dir}/{temp_name}"
        
        with open(temp_path, 'wb') as temp_file:
            temp_file.write(decrypted_data)
        
        return temp_path
    
    
encryption_service = FileEncryptionService()