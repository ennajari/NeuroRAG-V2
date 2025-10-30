"""
Script de test pour le client LLM
"""
from core.llm_client import llm_client
from core.embeddings import embedding_generator
from utils.logger import log

def test_llm():
    """Teste le client LLM"""
    log.info("=== TEST CLIENT LLM ===")
    
    # Test simple
    response = llm_client.chat(
        user_message="Dis bonjour en francais de maniere creative",
        system_prompt="Tu es un assistant IA amical et creatif"
    )
    
    print(f"\nReponse LLM:\n{response}\n")
    
    # Test cache (2e appel devrait etre instantane)
    log.info("Test cache (2e appel)...")
    response2 = llm_client.chat(
        user_message="Dis bonjour en francais de maniere creative",
        system_prompt="Tu es un assistant IA amical et creatif"
    )
    
    print(f"Cache fonctionne: {response == response2}\n")


def test_embeddings():
    """Teste le generateur d'embeddings"""
    log.info("=== TEST EMBEDDINGS ===")
    
    # Test simple
    text = "Ceci est un test pour generer des embeddings"
    embedding = embedding_generator.generate(text)
    
    print(f"Texte: {text}")
    print(f"Dimension embedding: {len(embedding)}")
    print(f"Premiers 5 valeurs: {embedding[:5]}\n")
    
    # Test cache
    log.info("Test cache embeddings...")
    embedding2 = embedding_generator.generate(text)
    
    print(f"Cache fonctionne: {embedding == embedding2}\n")
    
    # Test batch
    texts = [
        "Premier document sur l'IA",
        "Deuxieme document sur le machine learning",
        "Troisieme document sur les reseaux de neurones"
    ]
    
    embeddings = embedding_generator.generate_batch(texts)
    print(f"Batch embeddings: {len(embeddings)} vecteurs generes\n")


if __name__ == "__main__":
    try:
        test_llm()
        test_embeddings()
        log.info("=== TOUS LES TESTS REUSSIS ===")
    except Exception as e:
        log.error(f"Erreur dans les tests: {e}")
        raise
