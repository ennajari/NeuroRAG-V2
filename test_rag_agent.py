"""
Test de l'agent RAG complet
"""
from pathlib import Path
from ingestion.document_loader import document_loader
from ingestion.chunker import chunker
from knowledge.vector_store import vector_store
from agents.rag_agent import rag_agent
from utils.logger import log


def setup_test_data():
    """Prepare les donnees de test"""
    log.info("=== PREPARATION DONNEES TEST ===")
    
    # Creer un document de test plus riche
    test_dir = Path("data/documents/test")
    test_dir.mkdir(parents=True, exist_ok=True)
    
    test_file = test_dir / "ai_knowledge.txt"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("""
        Intelligence Artificielle et Machine Learning
        
        L'intelligence artificielle (IA) est un domaine de l'informatique qui vise a creer 
        des systemes capables de realiser des taches necessitant normalement l'intelligence humaine.
        
        Le machine learning est une branche de l'IA qui permet aux systemes d'apprendre 
        automatiquement a partir de donnees, sans etre explicitement programmes. 
        Il utilise des algorithmes statistiques pour identifier des patterns dans les donnees.
        
        Les reseaux de neurones sont inspires du fonctionnement du cerveau humain. 
        Ils sont composes de couches de neurones interconnectes qui traitent l'information 
        de maniere parallele.
        
        Le deep learning est une technique de machine learning qui utilise des reseaux 
        de neurones profonds avec plusieurs couches cachees. Cette approche a revolutionne 
        des domaines comme la vision par ordinateur et le traitement du langage naturel.
        
        Les systemes RAG (Retrieval Augmented Generation) combinent la recherche d'informations 
        et la generation de texte. Ils recherchent d'abord des documents pertinents dans une 
        base de connaissances, puis utilisent un LLM pour generer une reponse basee sur ces documents.
        """)
    
    print(f"Fichier de test cree: {test_file}")
    
    # Charger et indexer
    doc = document_loader.load(str(test_file))
    chunks = chunker.chunk_document(doc)
    
    print(f"Document charge: {len(chunks)} chunks")
    
    ids = vector_store.add_documents(chunks)
    
    print(f"Documents indexes: {len(ids)} IDs\n")


def test_rag_agent():
    """Teste l'agent RAG"""
    log.info("=== TEST AGENT RAG ===")
    
    questions = [
        "Qu'est-ce que le machine learning ?",
        "Comment fonctionnent les reseaux de neurones ?",
        "Qu'est-ce qu'un systeme RAG ?",
        "Quelle est la capitale de la France ?"  # Question hors contexte
    ]
    
    for i, question in enumerate(questions):
        print(f"\n{'='*60}")
        print(f"Question {i+1}: {question}")
        print('='*60)
        
        result = rag_agent.process({'query': question})
        
        print(f"\nReponse:\n{result['answer']}\n")
        
        if result['sources']:
            print(f"Sources ({len(result['sources'])}):")
            for source in result['sources']:
                print(f"  {source['index']}. Score: {source['score']:.3f}")
                print(f"     Preview: {source['preview'][:100]}...")
        else:
            print("Aucune source trouvee")
        
        print()


def cleanup():
    """Nettoie les donnees de test"""
    choice = input("\nSupprimer la collection de test ? (o/n): ")
    if choice.lower() == 'o':
        vector_store.delete_collection()
        log.info("Collection supprimee")


if __name__ == "__main__":
    try:
        setup_test_data()
        test_rag_agent()
        cleanup()
        log.info("=== TESTS REUSSIS ===")
    except Exception as e:
        log.error(f"Erreur: {e}")
        raise