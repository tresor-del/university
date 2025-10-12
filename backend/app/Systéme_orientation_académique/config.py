"""
Module pour charger et fournir la configuration globale du projet.
"""
import yaml
from functools import lru_cache

CONFIG_PATH = "config.yaml"

@lru_cache()
def get_config() -> dict:
    """Charge la configuration depuis le fichier YAML et la met en cache."""
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)
    return config