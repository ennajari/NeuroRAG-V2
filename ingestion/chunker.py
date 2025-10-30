"""
Decoupage intelligent de documents en chunks
"""
import re
from typing import List, Dict
from utils.logger import log


class Chunker:
    """Decoupe les documents en chunks avec overlap"""
    
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        separators: List[str] = None
    ):
        """
        Initialise le chunker
        
        Args:
            chunk_size: Taille max d'un chunk (en caracteres)
            chunk_overlap: Overlap entre chunks (en caracteres)
            separators: Separateurs pour le decoupage
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        if separators is None:
            self.separators = [
                "\n\n",
                "\n",
                ". ",
                "! ",
                "? ",
                "; ",
                ", ",
                " ",
                ""
            ]
        else:
            self.separators = separators
        
        log.info(f"Chunker initialise: size={chunk_size}, overlap={chunk_overlap}")
    
    def split_text(self, text: str) -> List[str]:
        """
        Decoupe le texte en chunks
        
        Args:
            text: Texte a decouper
            
        Returns:
            Liste de chunks
        """
        if len(text) <= self.chunk_size:
            return [text]
        
        chunks = []
        
        for separator in self.separators:
            if separator == "":
                chunks = self._split_by_chars(text)
                break
            
            if separator in text:
                chunks = self._split_by_separator(text, separator)
                
                if all(len(chunk) <= self.chunk_size * 1.2 for chunk in chunks):
                    break
        
        log.debug(f"Texte decoupe en {len(chunks)} chunks")
        
        return chunks
    
    def _split_by_separator(self, text: str, separator: str) -> List[str]:
        """Decoupe avec un separateur specifique"""
        parts = text.split(separator)
        chunks = []
        current_chunk = ""
        
        for part in parts:
            if part != parts[-1]:
                part += separator
            
            if len(current_chunk) + len(part) > self.chunk_size:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                
                if chunks and self.chunk_overlap > 0:
                    overlap_text = chunks[-1][-self.chunk_overlap:]
                    current_chunk = overlap_text + part
                else:
                    current_chunk = part
            else:
                current_chunk += part
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def _split_by_chars(self, text: str) -> List[str]:
        """Decoupage caractere par caractere (dernier recours)"""
        chunks = []
        
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
            chunk = text[i:i + self.chunk_size]
            chunks.append(chunk)
        
        return chunks
    
    def chunk_document(self, document: Dict) -> List[Dict]:
        """
        Decoupe un document en chunks avec metadata
        
        Args:
            document: Document a decouper (avec 'text', 'metadata', 'source')
            
        Returns:
            Liste de chunks avec metadata
        """
        text = document['text']
        chunks_text = self.split_text(text)
        
        chunks = []
        
        for i, chunk_text in enumerate(chunks_text):
            chunk = {
                'text': chunk_text,
                'metadata': {
                    **document['metadata'],
                    'chunk_index': i,
                    'total_chunks': len(chunks_text),
                    'chunk_size': len(chunk_text)
                },
                'source': document['source']
            }
            chunks.append(chunk)
        
        log.info(f"Document decoupe: {len(chunks)} chunks")
        
        return chunks


chunker = Chunker(chunk_size=1000, chunk_overlap=200)