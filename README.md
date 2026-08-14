# CipherGraph

**CipherGraph** is a Cyber Threat Intelligence (CTI) Analysis Platform that transforms unstructured threat intelligence reports into interactive knowledge graphs powered by AI.

## 🚀 Features

- **AI-Powered Entity Extraction**: Automatically extracts threat actors, indicators, victims, and tools from CTI reports using LLM technology
- **Interactive Knowledge Graph**: Visualize relationships between entities in a dynamic, hierarchical graph
- **Neo4j Integration**: Persistent graph database for complex threat intelligence queries
- **Real-time Processing**: Background task processing with status monitoring
- **Search & Investigation**: Search entities and investigate relationships with configurable depth
- **Modern UI**: Sleek, cybersecurity-themed dashboard built with vanilla JavaScript and vis-network

## 🛠️ Tech Stack

**Backend:**
- FastAPI (Python web framework)
- Neo4j (Graph database)
- OpenAI/OpenRouter API (LLM for entity extraction)
- Pydantic (Data validation)

**Frontend:**
- HTML5, CSS3, JavaScript
- vis-network (Graph visualization)
- Font Awesome (Icons)

**Infrastructure:**
- Docker & Docker Compose
- Uvicorn (ASGI server)

## 📋 Prerequisites

- Docker and Docker Compose
- OpenAI API key or OpenRouter API key
- Python 3.9+ (for local development)

## ⚙️ Installation

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/hurrainjhl/CIPHERGRAPH.git
cd CIPHERGRAPH
```

2. Configure environment variables:
```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env` and add your API keys:
```env
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
OPENAI_API_KEY=your_openai_api_key_here
# OR use OpenRouter
# OPENROUTER_API_KEY=your_openrouter_api_key_here
CIPHERGRAPH_API_KEY=your_secret_key_here
```

3. Start the services:
```bash
docker-compose up -d
```

4. Access the application:
- Web UI: http://localhost:8001
- Neo4j Browser: http://localhost:7474
- API Docs: http://localhost:8001/docs

### Local Development

1. Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Start Neo4j (via Docker):
```bash
docker run -d \
  --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  neo4j:5.21.0
```

3. Run the FastAPI server:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

## 🎯 Usage

### 1. Upload Threat Intelligence

Paste a CTI report or OSINT article into the text area and click **"Process Intelligence"**:

```
APT28, also known as Fancy Bear, targeted government agencies 
using Mimikatz and PowerShell scripts. They compromised systems 
at example.gov via phishing campaigns distributing malware through 
malicious domains like evil-domain.com (192.168.1.100).
```

### 2. View the Knowledge Graph

The system will extract entities and relationships, displaying them in an interactive graph:
- **Red nodes**: Threat actors/attackers
- **Cyan nodes**: Indicators (IPs, domains)
- **Green nodes**: Victims/targets
- **Purple nodes**: Tools/malware

### 3. Investigate Entities

- Click any node to see details in the investigation panel
- Search for specific entities using the search bar
- Filter entities by type (Attacker, Indicator, Victim, Tool)
- Double-click to focus and investigate relationships

## 📡 API Endpoints

### POST `/episodes`
Upload and process a CTI report
```json
{
  "content": "Your threat intelligence text...",
  "group_id": "campaign-name"
}
```

### GET `/episodes/tasks/{task_id}`
Check processing status

### GET `/episodes/list`
List all processed episodes

### GET `/episodes/{episode_id}/graph`
Retrieve graph data for a specific episode

### POST `/search/nodes`
Search for entities
```json
{
  "query": "APT28",
  "group_id": "default",
  "limit": 20
}
```

### POST `/investigate`
Investigate entity relationships
```json
{
  "entity_name": "APT28",
  "depth": 2,
  "group_id": "default"
}
```

### GET `/health`
Health check endpoint

## 🔐 Security

- API endpoints are protected with API key authentication via `X-CipherGraph-Key` header
- Configure `CIPHERGRAPH_API_KEY` in environment variables
- Health check endpoint is public

## 🏗️ Project Structure

```
ciphergraph/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── database.py      # Neo4j connection
│   │   │   └── llm.py           # LLM integration
│   │   ├── models/
│   │   │   └── api.py           # Pydantic models
│   │   ├── services/
│   │   │   └── graph_service.py # Graph operations
│   │   └── main.py              # FastAPI app
│   ├── config/
│   │   └── settings.py          # Configuration
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env
├── frontend/
│   └── index.html               # Single-page app
└── docker-compose.yml
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Neo4j](https://neo4j.com/) - Graph database
- [vis-network](https://visjs.github.io/vis-network/) - Graph visualization
- [OpenAI](https://openai.com/) / [OpenRouter](https://openrouter.ai/) - LLM APIs

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ for the cybersecurity community**
