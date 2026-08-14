from fastapi import FastAPI, BackgroundTasks, Header, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.core.database import Neo4jDriver
from app.services.graph_service import GraphService
from app.models.api import AddEpisodeRequest, SearchNodesRequest, InvestigateRequest
from config.settings import settings
import uuid
import logging

graph_service = GraphService()
logger = logging.getLogger("ciphergraph")
logging.basicConfig(level=logging.INFO)

INGESTION_TASKS = {}

async def run_extraction_task(task_id: str, content: str, group_id: str):
    try:
        logger.info(f"Starting extraction task {task_id}")
        INGESTION_TASKS[task_id] = {
            "status": "processing",
            "entities": 0,
            "relationships": 0,
            "episode_id": None,
            "error": None
        }
        result = await graph_service.add_episode(content, group_id)
        if result.get("success"):
            INGESTION_TASKS[task_id] = {
                "status": "completed",
                "entities": result.get("entities", 0),
                "relationships": result.get("relationships", 0),
                "episode_id": result.get("episode_id"),
                "error": None
            }
            logger.info(f"Task {task_id} completed: {result.get('entities', 0)} entities, {result.get('relationships', 0)} relationships")
        else:
            INGESTION_TASKS[task_id] = {
                "status": "failed",
                "entities": 0,
                "relationships": 0,
                "episode_id": None,
                "error": result.get("detail", "Extraction failed")
            }
    except Exception as e:
        logger.error(f"Task {task_id} failed: {e}")
        INGESTION_TASKS[task_id] = {
            "status": "failed",
            "entities": 0,
            "relationships": 0,
            "episode_id": None,
            "error": str(e)
        }

async def verify_api_key(x_ciphergraph_key: str = Header(None)):
    if settings.api_key:
        if x_ciphergraph_key != settings.api_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access Denied: Invalid or missing API key."
            )

@asynccontextmanager
async def lifespan(app: FastAPI):
    await Neo4jDriver.connect()
    if not Neo4jDriver.connected:
        logger.warning("Neo4j is unavailable. Graph endpoints will return 503 until the database is running.")
    yield
    await Neo4jDriver.close()

app = FastAPI(title="CipherGraph API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/episodes")
async def add_episode(req: AddEpisodeRequest, background_tasks: BackgroundTasks, auth: None = Depends(verify_api_key)):
    task_id = str(uuid.uuid4())
    INGESTION_TASKS[task_id] = {
        "status": "pending",
        "entities": 0,
        "relationships": 0,
        "episode_id": None,
        "error": None
    }
    background_tasks.add_task(run_extraction_task, task_id, req.content, req.group_id)
    return {"success": True, "task_id": task_id, "status": "pending"}

@app.get("/episodes/tasks/{task_id}")
async def get_task_status(task_id: str):
    task = INGESTION_TASKS.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Ingestion task not found.")
    return task

@app.get("/episodes/list")
async def list_all_episodes(auth: None = Depends(verify_api_key)):
    episodes = await graph_service.get_all_episodes()
    return {"success": True, "episodes": episodes}

@app.get("/episodes/{episode_id}/graph")
async def get_episode_graph(episode_id: str, auth: None = Depends(verify_api_key)):
    graph = await graph_service.get_episode_graph(episode_id)
    return {"success": True, "graph": graph}

@app.post("/search/nodes")
async def search_nodes(req: SearchNodesRequest, auth: None = Depends(verify_api_key)):
    nodes = await graph_service.search_nodes(req.query, req.group_id, req.limit)
    return nodes

@app.post("/investigate")
async def investigate_entity(req: InvestigateRequest, auth: None = Depends(verify_api_key)):
    graph = await graph_service.investigate_entity(req.entity_name, req.depth, req.group_id)
    return graph

@app.get("/health")
async def health_check():
    return {"status": "ok", "neo4j_connected": Neo4jDriver.connected}

app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
