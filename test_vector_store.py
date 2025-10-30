
"""
Test du vector store
"""
from ingestion.document_loader import document_loader
from ingestion.chunker import chunker
from knowledge.vector_store import vector_store
from utils.logger import log
from pathlib import Path


def test_vector_store():
    """Teste le vector store complet"""
    log.info("=== TEST VECTOR STORE ===")
    
    # Charger document de test
    test_file = Path("data/documents/test/test.txt")
    
    if not test_file.exists():
        log.error("Fichier de test introuvable. Lance d'abord: python test_ingestion.py")
        return
    
    doc = document_loader.load(str(test_file))
    chunks = chunker.chunk_document(doc)
    
    print(f"\nDocument charge et decoupe: {len(chunks)} chunks")
    
    # Ajouter au vector store
    ids = vector_store.add_documents(chunks)
    print(f"Documents ajoutes: {len(ids)} IDs")
    
    # Infos collection
    info = vector_store.get_collection_info()
    print(f"\nCollection info:")
    print(f"  Nom: {info['name']}")
    print(f"  Points: {info['points_count']}")
    print(f"  Status: {info['status']}")
    
    # Recherche
    query = "Qu'est-ce que le machine learning ?"
    results = vector_store.search(query, limit=3, score_threshold=0.3)
    
    print(f"\nRecherche: '{query}'")
    print(f"Resultats: {len(results)}\n")
    
    for i, result in enumerate(results):
        print(f"Resultat {i+1}:")
        print(f"  Score: {result['score']:.3f}")
        print(f"  Texte: {result['text'][:100]}...")
        print()


def test_cleanup():
    """Nettoie le vector store"""
    choice = input("\nSupprimer la collection de test ? (o/n): ")
    if choice.lower() == 'o':
        vector_store.delete_collection()
        log.info("Collection supprimee")


if __name__ == "__main__":
    try:
        test_vector_store()
        test_cleanup()
        log.info("=== TESTS REUSSIS ===")
    except Exception as e:
        log.error(f"Erreur: {e}")
        raise