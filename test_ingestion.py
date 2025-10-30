"""
Test du systeme d'ingestion
"""
from pathlib import Path
from ingestion.document_loader import document_loader
from ingestion.chunker import chunker
from utils.logger import log


def create_test_files():
    """Cree des fichiers de test"""
    test_dir = Path("data/documents/test")
    test_dir.mkdir(parents=True, exist_ok=True)
    
    txt_file = test_dir / "test.txt"
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write("""
        Ceci est un document de test pour le systeme NeuroRAG.
        
        Il contient plusieurs paragraphes pour tester le decoupage en chunks.
        
        L'intelligence artificielle revolutionne de nombreux domaines.
        Les systemes de RAG permettent de combiner recherche et generation.
        
        Ce texte est suffisamment long pour etre decoupe en plusieurs chunks
        et tester le mecanisme d'overlap entre les chunks.
        
        Le machine learning est une branche de l'IA qui permet aux systemes
        d'apprendre a partir de donnees sans etre explicitement programmes.
        """)
    
    log.info(f"Fichiers de test crees dans: {test_dir}")
    return test_dir


def test_document_loading():
    """Teste le chargement de documents"""
    log.info("=== TEST CHARGEMENT DOCUMENTS ===")
    
    test_dir = create_test_files()
    test_file = test_dir / "test.txt"
    
    doc = document_loader.load(str(test_file))
    
    print(f"\nDocument charge:")
    print(f"  Source: {doc['source']}")
    print(f"  Taille: {doc['metadata']['num_chars']} caracteres")
    print(f"  Nom: {doc['metadata']['filename']}")
    print(f"\nPreview texte:\n{doc['text'][:200]}...\n")


def test_chunking():
    """Teste le decoupage en chunks"""
    log.info("=== TEST DECOUPAGE EN CHUNKS ===")
    
    test_dir = Path("data/documents/test")
    test_file = test_dir / "test.txt"
    doc = document_loader.load(str(test_file))
    
    chunks = chunker.chunk_document(doc)
    
    print(f"\nDocument decoupe en {len(chunks)} chunks:\n")
    
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}/{len(chunks)}:")
        print(f"  Taille: {chunk['metadata']['chunk_size']} caracteres")
        print(f"  Preview: {chunk['text'][:100]}...")
        print()


def test_directory_loading():
    """Teste le chargement d'un dossier"""
    log.info("=== TEST CHARGEMENT DOSSIER ===")
    
    test_dir = Path("data/documents/test")
    
    documents = document_loader.load_directory(str(test_dir))
    
    print(f"\nDossier charge: {len(documents)} documents")
    
    for doc in documents:
        print(f"  - {doc['metadata']['filename']}: {doc['metadata']['num_chars']} caracteres")


if __name__ == "__main__":
    try:
        test_document_loading()
        test_chunking()
        test_directory_loading()
        log.info("=== TOUS LES TESTS REUSSIS ===")
    except Exception as e:
        log.error(f"Erreur dans les tests: {e}")
        raise