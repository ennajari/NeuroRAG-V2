"""
Agent RAG simple combinant recherche et generation
"""
from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from knowledge.vector_store import vector_store
from core.llm_client import llm_client
from config.settings import settings
from utils.logger import log


class RAGAgent(BaseAgent):
    """Agent RAG: Retrieval Augmented Generation"""
    
    def __init__(self, name: str = "RAG Agent"):
        """Initialise l'agent RAG"""
        super().__init__(name)
        self.vector_store = vector_store
        self.llm = llm_client
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Traite une question avec RAG
        
        Args:
            input_data: Dict avec 'query' (question)
            
        Returns:
            Dict avec 'answer', 'sources', 'context'
        """
        query = input_data.get('query', '')
        
        if not query:
            return {
                'answer': 'Erreur: Aucune question fournie',
                'sources': [],
                'context': []
            }
        
        log.info(f"Question recue: {query}")
        
        # Etape 1: Recherche dans le vector store
        search_results = self._retrieve(query)
        
        if not search_results:
            return {
                'answer': 'Desole, je n\'ai trouve aucune information pertinente dans ma base de connaissances.',
                'sources': [],
                'context': []
            }
        
        # Etape 2: Generer la reponse avec le contexte
        answer = self._generate(query, search_results)
        
        # Etape 3: Formater les sources
        sources = self._format_sources(search_results)
        
        return {
            'answer': answer,
            'sources': sources,
            'context': [r['text'] for r in search_results]
        }
    
    def _retrieve(self, query: str, limit: int = 3) -> List[Dict]:
        """Recherche les documents pertinents"""
        log.info(f"Recherche documents pour: {query}")
        
        # Adapter le threshold selon la requete
        if len(query.split()) <= 2:  # Requete courte
            threshold = 0.0
        else:  # Requete longue
            threshold = 0.3
        
        results = self.vector_store.search(
            query=query,
            limit=limit,
            score_threshold=threshold
        )
        
        log.info(f"Documents trouves: {len(results)}")
        
        return results
    
    def _generate(self, query: str, context_docs: List[Dict]) -> str:
        """
        Genere une reponse avec le contexte
        
        Args:
            query: Question
            context_docs: Documents de contexte
            
        Returns:
            Reponse generee
        """
        # Construire le contexte
        context_text = "\n\n".join([
            f"Document {i+1} (score: {doc['score']:.2f}):\n{doc['text']}"
            for i, doc in enumerate(context_docs)
        ])
        
        # Prompt systeme
        system_prompt = """You are an intelligent AI assistant that answers questions using only the information provided in the context.

    CRITICAL RULES:
    - ALWAYS respond in the SAME LANGUAGE as the user's question
    - If the question is in English, respond in English
    - If the question is in French, respond in French  
    - If the question is in Arabic/Amazigh, respond in Arabic/Amazigh
    - If the question is in any other language, respond in that language
    - Answer ONLY with information from the context
    - If the information is not in the context, say so clearly in the user's language
    - Be precise and concise
    - Cite sources when relevant"""
        
        # Prompt utilisateur
        user_prompt = f"""Context:
    {context_text}

    Question: {query}

    Answer the question using ONLY the information from the context above. 
    IMPORTANT: Respond in the SAME LANGUAGE as the question."""
        
        log.info("Generation de la reponse...")
        
        # Appel LLM
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        answer = self.llm.generate(messages)
        
        log.info("Reponse generee")
        
        return answer
    
    def _format_sources(self, results: List[Dict]) -> List[Dict]:
        """
        Formate les sources pour l'affichage
        
        Args:
            results: Resultats de recherche
            
        Returns:
            Sources formatees
        """
        sources = []
        
        for i, result in enumerate(results):
            source = {
                'index': i + 1,
                'score': result['score'],
                'source': result.get('source', 'Unknown'),
                'metadata': result.get('metadata', {}),
                'preview': result['text'][:200] + '...' if len(result['text']) > 200 else result['text']
            }
            sources.append(source)
        
        return sources


rag_agent = RAGAgent()