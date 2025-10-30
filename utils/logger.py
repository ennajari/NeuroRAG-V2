"""
Systeme de logging configure avec Loguru
"""
import sys
from pathlib import Path
from loguru import logger
from config.settings import settings


def setup_logger():
    """Configure le logger"""
    
    # Supprimer le handler par defaut
    logger.remove()
    
    # Console handler (coloré)
    logger.add(
        sys.stdout,
        level=settings.LOG_LEVEL,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        colorize=True
    )
    
    # Fichier handler (tous les logs)
    logger.add(
        settings.LOGS_DIR / "neurorag.log",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}",
        rotation="10 MB",
        retention="30 days",
        compression="zip"
    )
    
    # Fichier handler (erreurs seulement)
    logger.add(
        settings.LOGS_DIR / "errors.log",
        level="ERROR",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}",
        rotation="10 MB",
        retention="90 days",
        compression="zip"
    )
    
    return logger


# Logger global
log = setup_logger()
