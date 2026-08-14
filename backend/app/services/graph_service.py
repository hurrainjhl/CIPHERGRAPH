import uuid
import logging
from typing import Dict, Any, List
from app.core.database import Neo4jDriver
from app.core.llm import extract_entities

logger = logging.getLogger("ciphergraph")

class GraphService:
    def __init__(self):
        pass

    def _get_session(self):
        return Neo4jDriver.driver.session()
        
    def _using_neo4j(self):
        return Neo4jDriver.connected

    async def add_episode(self, content: str, group_id: str = "default") -> Dict[str, Any]:
        extracted = await extract_entities(content)
        entities = extracted.get("entities", [])
        relationships = extracted.get("relationships", [])
        
        episode_uuid = str(uuid.uuid4())
        
        if self._using_neo4j():
            async with self._get_session() as session:
                await session.run(
                    "CREATE (e:Episodic {uuid: $uuid, content: $content, created_at: datetime()})",
                    uuid=episode_uuid, content=content
                )
                
                for entity in entities:
                    await session.run(
                        """
                        MERGE (n:Entity {name: $name, group_id: $episode_uuid})
                        ON CREATE SET n.uuid = randomUUID(), n.type = $type, n.summary = $summary
                        """,
                        name=entity["name"], type=entity["type"], summary=entity.get("summary", ""), episode_uuid=episode_uuid
                    )
                    
                for rel in relationships:
                    await session.run(
                        """
                        MATCH (s:Entity {name: $source, group_id: $episode_uuid})
                        MATCH (t:Entity {name: $target, group_id: $episode_uuid})
                        MERGE (s)-[r:RELATES_TO {type: $type}]->(t)
                        ON CREATE SET r.fact = $fact
                        """,
                        source=rel["source"], target=rel["target"], type=rel["type"], fact=rel.get("fact", ""), episode_uuid=episode_uuid
                    )
                    
        return {
            "success": True, 
            "episode_id": episode_uuid,
            "entities": len(entities), 
            "relationships": len(relationships)
        }

    async def get_all_episodes(self) -> List[Dict[str, Any]]:
        if self._using_neo4j():
            async with self._get_session() as session:
                result = await session.run("MATCH (e:Episodic) RETURN e.uuid AS id, e.content AS content, e.created_at AS date ORDER BY e.created_at DESC LIMIT 50")
                return await result.data()
        return []

    async def get_episode_graph(self, episode_id: str) -> Dict[str, Any]:
        if self._using_neo4j():
            async with self._get_session() as session:
                nodes_res = await session.run(
                    "MATCH (n:Entity {group_id: $episode_id}) RETURN n.uuid AS id, n.name AS label, n.summary AS title, n.type AS group",
                    episode_id=episode_id
                )
                nodes = await nodes_res.data()

                edges_res = await session.run(
                    """MATCH (s:Entity {group_id: $episode_id})-[r]->(t:Entity {group_id: $episode_id}) 
                       RETURN s.uuid AS from, t.uuid AS to, r.type AS label, r.fact AS title""",
                    episode_id=episode_id
                )
                edges = await edges_res.data()
                return {"nodes": nodes, "edges": edges}
        return {"nodes": [], "edges": []}

    async def search_nodes(self, query: str, group_id: str, limit: int = 50) -> Dict[str, Any]:
        if self._using_neo4j():
            async with self._get_session() as session:
                res = await session.run(
                    """
                    MATCH (n:Entity {group_id: $group_id})
                    WHERE toLower(n.name) CONTAINS toLower($query) OR toLower(n.type) CONTAINS toLower($query)
                    RETURN n.uuid AS id, n.name AS label, n.summary AS title, n.type AS group LIMIT $limit
                    """,
                    query=query, group_id=group_id, limit=limit
                )
                nodes = await res.data()
                return {"nodes": nodes}
        return {"nodes": []}
        
    async def investigate_entity(self, entity_name: str, depth: int, group_id: str) -> Dict[str, Any]:
        if self._using_neo4j():
            async with self._get_session() as session:
                res = await session.run(
                    """
                    MATCH (n:Entity {name: $name, group_id: $group_id})-[r*1..2]-(m:Entity {group_id: $group_id})
                    RETURN n, r, m
                    """,
                    name=entity_name, group_id=group_id
                )
                nodes_set = {}
                edges_list = []
                async for record in res:
                    n = record["n"]
                    m = record["m"]
                    rels = record["r"]
                    for node in [n, m]:
                        if node.id not in nodes_set:
                            nodes_set[node.id] = {
                                "id": node["uuid"],
                                "label": node["name"],
                                "title": node.get("summary", ""),
                                "group": node.get("type", "Entity")
                            }
                    for rel in rels:
                        edges_list.append({
                            "from": rel.nodes[0]["uuid"],
                            "to": rel.nodes[1]["uuid"],
                            "label": rel["type"],
                            "title": rel.get("fact", "")
                        })
                return {"nodes": list(nodes_set.values()), "edges": edges_list}
        return {"nodes": [], "edges": []}
