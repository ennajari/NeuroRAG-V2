"""
Client LLM avec gestion d'erreurs, retry et cache
"""
import json
import hashlib
from pathlib import Path
from typing import Optional, List, Dict, Any
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
from config.settings import settings
from utils.logger import log


class LLMClient:
    """Client pour interagir avec OpenAI"""
    
    def __init__(self):
        """Initialise le client OpenAI"""
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY manquante dans .env")
        
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.cache_dir = settings.CACHE_DIR / "llm_cache"
        self.cache_dir.mkdir(exist_ok=True)
        
        log.info(f"Client LLM initialise avec modele: {self.model}")
    
    def _get_cache_key(self, messages: List[Dict], **kwargs) -> str:
        """Genere une cle de cache unique"""
        cache_str = json.dumps({
            "messages": messages,
            "model": self.model,
            **kwargs
        }, sort_keys=True)
        return hashlib.md5(cache_str.encode()).hexdigest()
    
    def _get_from_cache(self, cache_key: str) -> Optional[str]:
        """Recupere une reponse du cache"""
        cache_file = self.cache_dir / f"{cache_key}.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    log.debug(f"Cache hit: {cache_key}")
                    return data['response']
            except Exception as e:
                log.warning(f"Erreur lecture cache: {e}")
        return None
    
    def _save_to_cache(self, cache_key: str, response: str):
        """Sauvegarde une reponse dans le cache"""
        cache_file = self.cache_dir / f"{cache_key}.json"
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump({'response': response}, f, ensure_ascii=False)
            log.debug(f"Cache saved: {cache_key}")
        except Exception as e:
            log.warning(f"Erreur ecriture cache: {e}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        use_cache: bool = True
    ) -> str:
        """
        Genere une reponse avec le LLM
        
        Args:
            messages: Liste de messages (role: user/assistant/system, content: texte)
            temperature: Temperature de generation (0-2)
            max_tokens: Nombre max de tokens
            use_cache: Utiliser le cache ou non
            
        Returns:
            Reponse du LLM
        """
        temp = temperature or settings.OPENAI_TEMPERATURE
        max_tok = max_tokens or settings.OPENAI_MAX_TOKENS
        
        # Verifier le cache
        if use_cache:
            cache_key = self._get_cache_key(messages, temperature=temp, max_tokens=max_tok)
            cached_response = self._get_from_cache(cache_key)
            if cached_response:
                return cached_response
        
        # Appel API
        try:
            log.info(f"Appel LLM: {len(messages)} messages")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temp,
                max_tokens=max_tok
            )
            
            content = response.choices[0].message.content
            
            # Sauvegarder dans le cache
            if use_cache:
                self._save_to_cache(cache_key, content)
            
            # Logger les tokens utilises
            usage = response.usage
            log.info(f"Tokens utilises: {usage.total_tokens} (prompt: {usage.prompt_tokens}, completion: {usage.completion_tokens})")
            
            return content
            
        except Exception as e:
            log.error(f"Erreur appel LLM: {e}")
            raise
    
    def chat(self, user_message: str, system_prompt: Optional[str] = None) -> str:
        """
        Methode simple pour un chat
        
        Args:
            user_message: Message de l'utilisateur
            system_prompt: Prompt systeme optionnel
            
        Returns:
            Reponse du LLM
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": user_message})
        
        return self.generate(messages)


# Instance globale
llm_client = LLMClient()
