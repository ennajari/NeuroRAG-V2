# NeuroRAG V2.0

Systeme d'IA avance combinant Multi-Agents, GraphRAG et Memoire Cognitive pour des reponses contextuelles intelligentes.

## Fonctionnalites

- **Ingestion Multi-Format**: PDF, TXT, DOCX avec decoupage intelligent en chunks
- **Recherche Semantique**: Vector database Qdrant avec embeddings OpenAI
- **Agent RAG**: Retrieval Augmented Generation avec citations de sources
- **Interface Web**: Application Streamlit interactive
- **Cache Intelligent**: Reduction des couts API avec mise en cache automatique
- **Logging Complet**: Suivi detaille avec Loguru

## Architecture
```
NeuroRAG V2.0
├── Ingestion Layer
│   ├── Document Loader (PDF, TXT, DOCX)
│   └── Smart Chunker (overlap-based)
│
├── Knowledge Layer
│   ├── Vector Store (Qdrant)
│   └── Embeddings (OpenAI text-embedding-3-small)
│
├── Agent Layer
│   ├── RAG Agent
│   └── LLM Client (GPT-4o-mini)
│
└── Interface Layer
    └── Streamlit Web App
```

## Technologies

- **LLM**: OpenAI GPT-4o-mini
- **Embeddings**: text-embedding-3-small (1536 dimensions)
- **Vector DB**: Qdrant
- **Framework**: LangChain
- **Backend**: FastAPI (futur)
- **Frontend**: Streamlit
- **Languages**: Python 3.11+

## Installation

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Cle API OpenAI

### Setup
```bash
# Cloner le repository
git clone https://github.com/ennajari/NeuroRAG-V2.git
cd NeuroRAG-V2

# Creer environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Installer dependances
pip install -r requirements.txt

# Lancer services (Qdrant + Neo4j)
docker-compose up -d

# Configurer variables environnement
cp .env.example .env
# Editer .env et ajouter votre OPENAI_API_KEY
```

### Configuration

Editer `.env`:
```env
OPENAI_API_KEY=votre_cle_api
OPENAI_MODEL=gpt-4o-mini
QDRANT_HOST=localhost
QDRANT_PORT=6333
```

## Utilisation

### Interface Web
```bash
streamlit run frontend/app.py
```

Ouvrir http://localhost:8501

### Utilisation Programmatique
```python
from ingestion.document_loader import document_loader
from ingestion.chunker import chunker
from knowledge.vector_store import vector_store
from agents.rag_agent import rag_agent

# Charger et indexer un document
doc = document_loader.load("mon_document.pdf")
chunks = chunker.chunk_document(doc)
vector_store.add_documents(chunks)

# Poser une question
result = rag_agent.process({'query': 'Quelle est la reponse ?'})
print(result['answer'])
print(f"Sources: {len(result['sources'])}")
```

## Tests
```bash
# Test client LLM
python test_llm.py

# Test ingestion
python test_ingestion.py

# Test vector store
python test_vector_store.py

# Test agent RAG complet
python test_rag_agent.py
```

## Structure du Projet
```
NeuroRAG-V2/
├── config/              # Configuration
│   ├── __init__.py
│   ├── settings.py      # Configuration globale
│   └── prompts.py       # Templates de prompts
│
├── core/                # Composants centraux
│   ├── __init__.py
│   ├── llm_client.py    # Client OpenAI avec cache
│   └── embeddings.py    # Generation embeddings
│
├── agents/              # Systeme multi-agents
│   ├── __init__.py
│   ├── base_agent.py    # Classe de base
│   └── rag_agent.py     # Agent RAG
│
├── memory/              # Memoire cognitive (futur)
│   └── __init__.py
│
├── knowledge/           # Gestion connaissances
│   ├── __init__.py
│   └── vector_store.py  # Interface Qdrant
│
├── ingestion/           # Ingestion documents
│   ├── __init__.py
│   ├── document_loader.py
│   └── chunker.py
│
├── api/                 # API REST (futur)
│   └── __init__.py
│
├── frontend/            # Interface utilisateur
│   └── app.py           # Application Streamlit
│
├── utils/               # Utilitaires
│   ├── __init__.py
│   ├── logger.py        # Systeme de logs
│   └── cache.py         # Gestion cache
│
├── data/                # Donnees locales
│   ├── documents/       # Documents sources
│   ├── cache/           # Cache embeddings/LLM
│   └── logs/            # Fichiers de logs
│
├── tests/               # Tests unitaires
│
├── docker-compose.yml   # Services Docker
├── requirements.txt     # Dependances Python
├── .env.example         # Template variables env
└── README.md
```

## Performances

- **Latence moyenne**: 2-3 secondes par requete
- **Precision recherche**: Score moyen >0.4 pour requetes pertinentes
- **Cache hit rate**: ~60% sur requetes repetees
- **Cout par requete**: ~0.002$ (GPT-4o-mini)

## Roadmap

### Phase 1: MVP - RAG Basique (TERMINE)
- [x] Structure projet
- [x] Client LLM avec cache
- [x] Ingestion documents
- [x] Vector Store Qdrant
- [x] Agent RAG simple
- [x] Interface Streamlit

### Phase 2: Multi-Agents System (En cours)
- [ ] Orchestrator Agent
- [ ] Retrieval Agent specialise
- [ ] Reasoning Agent
- [ ] Integration LangGraph
- [ ] Memoire court terme

### Phase 3: Knowledge Graph
- [ ] Integration Neo4j
- [ ] Extraction entites (NER)
- [ ] Relations semantiques
- [ ] Visualisation 3D
- [ ] Memoire long terme

### Phase 4: Vision & Optimisation
- [ ] OCR (Tesseract)
- [ ] Analyse images (GPT-4 Vision)
- [ ] Optimisation couts API
- [ ] API REST FastAPI
- [ ] Deploiement production

## Contributeurs

**Abdellah Ennajari**
- Etudiant Ingenieur IA - ENIAD
- LinkedIn: [votre-profil](www.linkedin.com/in/ennajari-abdellah)
- Email: abdellahennajari2018@gmail.com

## Licence

MIT License - Voir [LICENSE](LICENSE) pour details

## Remerciements

- OpenAI pour les modeles GPT-4o-mini et embeddings
- Qdrant pour la vector database
- Communaute LangChain pour les outils RAG