"""
Interface avec Qdrant pour stockage vectoriel
"""
import uuid
from typing import List, Dict, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from config.settings import settings
from core.embeddings import embedding_generator
from utils.logger import log


class VectorStore:
    """Gestionnaire du vector store Qdrant"""
    
    def __init__(self):
        """Initialise la connexion Qdrant"""
        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT
        )
        self.collection_name = settings.QDRANT_COLLECTION_NAME
        
        log.info(f"VectorStore initialise: {settings.QDRANT_HOST}:{settings.QDRANT_PORT}")
        
        self._ensure_collection_exists()
    
    def _ensure_collection_exists(self):
        """Cree la collection si elle n'existe pas"""
        collections = self.client.get_collections().collections
        collection_names = [col.name for col in collections]
        
        if self.collection_name not in collection_names:
            log.info(f"Creation collection: {self.collection_name}")
            
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=settings.EMBEDDING_DIMENSION,
                    distance=Distance.COSINE
                )
            )
        else:
            log.info(f"Collection existante: {self.collection_name}")
    
    def add_documents(self, documents: List[Dict]) -> List[str]:
        """
        Ajoute des documents au vector store
        
        Args:
            documents: Liste de documents avec 'text', 'metadata', 'source'
            
        Returns:
            Liste des IDs crees
        """
        if not documents:
            return []
        
        log.info(f"Ajout de {len(documents)} documents")
        
        points = []
        ids = []
        
        for doc in documents:
            text = doc['text']
            
            embedding = embedding_generator.generate(text)
            
            point_id = str(uuid.uuid4())
            ids.append(point_id)
            
            point = PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    'text': text,
                    'metadata': doc.get('metadata', {}),
                    'source': doc.get('source', '')
                }
            )
            
            points.append(point)
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        
        log.info(f"{len(points)} documents ajoutes au vector store")
        
        return ids
    
    def search(
        self,
        query: str,
        limit: int = 5,
        score_threshold: float = 0.5
    ) -> List[Dict]:
        """
        Recherche par similarite
        
        Args:
            query: Question/requete
            limit: Nombre de resultats
            score_threshold: Score minimum de pertinence
            
        Returns:
            Liste de resultats avec score
        """
        log.info(f"Recherche: '{query}' (limit={limit})")
        
        query_embedding = embedding_generator.generate(query)
        
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit,
            score_threshold=score_threshold
        )
        
        formatted_results = []
        
        for result in results:
            formatted_results.append({
                'id': result.id,
                'score': result.score,
                'text': result.payload.get('text', ''),
                'metadata': result.payload.get('metadata', {}),
                'source': result.payload.get('source', '')
            })
        
        log.info(f"{len(formatted_results)} resultats trouves")
        
        return formatted_results
    
    def delete_collection(self):
        """Supprime la collection"""
        log.warning(f"Suppression collection: {self.collection_name}")
        self.client.delete_collection(collection_name=self.collection_name)
    
    def get_collection_info(self) -> Dict:
        """Recupere les infos de la collection"""
        info = self.client.get_collection(collection_name=self.collection_name)
        
        return {
            'name': self.collection_name,
            'points_count': info.points_count,
            'vectors_count': info.vectors_count,
            'status': info.status
        }


vector_store = VectorStore()