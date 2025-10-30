"""
Classe de base pour tous les agents
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
from utils.logger import log


class BaseAgent(ABC):
    """Classe abstraite pour tous les agents"""
    
    def __init__(self, name: str):
        """
        Initialise l'agent
        
        Args:
            name: Nom de l'agent
        """
        self.name = name
        log.info(f"Agent initialise: {name}")
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Traite une requete
        
        Args:
            input_data: Donnees d'entree
            
        Returns:
            Resultat du traitement
        """
        pass
    
    def __str__(self):
        return f"{self.__class__.__name__}(name={self.name})"