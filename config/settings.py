"""
Configuration globale de l'application
"""
import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Charger .env
load_dotenv()

# Dossier racine du projet
ROOT_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    """Configuration de l'application"""
    
    # Application
    APP_NAME: str = os.getenv("APP_NAME", "NeuroRAG V2.0")
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "True").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_TEMPERATURE: float = 0.7
    OPENAI_MAX_TOKENS: int = 2000
    
    # Embeddings
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    EMBEDDING_DIMENSION: int = 1536
    
    # Qdrant
    QDRANT_HOST: str = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT: int = int(os.getenv("QDRANT_PORT", "6333"))
    QDRANT_COLLECTION_NAME: str = os.getenv("QDRANT_COLLECTION_NAME", "neurorag")
    
    # Neo4j
    NEO4J_URI: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER: str = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "neurorag2024")
    
    # Paths
    DATA_DIR: Path = ROOT_DIR / "data"
    DOCUMENTS_DIR: Path = DATA_DIR / "documents"
    CACHE_DIR: Path = DATA_DIR / "cache"
    LOGS_DIR: Path = DATA_DIR / "logs"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # AJOUT: Ignore les variables non declarees


# Instance globale
settings = Settings()


# Creer les dossiers si necessaire
for directory in [settings.DOCUMENTS_DIR, settings.CACHE_DIR, settings.LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
