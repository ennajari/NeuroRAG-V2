# NeuroRAG V2.0

Systeme d'IA avance avec Multi-Agents, GraphRAG et Memoire Cognitive

## Installation
```bash
# Creer environnement virtuel
python -m venv .env
source .env/bin/activate  # Linux/Mac
# ou
.env\Scripts\activate  # Windows

# Installer dependances
pip install -r requirements.txt

# Lancer les services (Qdrant + Neo4j)
docker-compose up -d

# Configurer variables environnement
cp .env.example .env
# Editer .env avec vos cles API
```

## Structure du projet
```
neurorag-v2/
├── config/          # Configuration
├── core/            # Client LLM et embeddings
├── agents/          # Systeme multi-agents
├── memory/          # Memoire cognitive
├── knowledge/       # Knowledge Graph + Vector DB
├── ingestion/       # Ingestion documents
├── api/             # API FastAPI
├── frontend/        # Interface Streamlit
├── utils/           # Utilitaires
├── data/            # Donnees locales
└── tests/           # Tests
```

## Utilisation
```bash
# Lancer l'interface Streamlit
streamlit run frontend/app.py

# Ou lancer l'API
uvicorn api.main:app --reload
```

## Technologies

- OpenAI GPT-4o-mini
- LangChain + LangGraph
- Qdrant (Vector Database)
- Neo4j (Knowledge Graph)
- FastAPI
- Streamlit

## Licence

MIT