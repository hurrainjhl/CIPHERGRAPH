from neo4j import AsyncGraphDatabase
import logging
from config.settings import settings

logger = logging.getLogger("ciphergraph")

class Neo4jConnection:
    def __init__(self):
        self.driver = None
        self.connected = False

    async def connect(self):
        try:
            self.driver = AsyncGraphDatabase.driver(
                settings.neo4j_uri,
                auth=(settings.neo4j_user, settings.neo4j_password)
            )
            await self.driver.verify_connectivity()
            self.connected = True
            logger.info("Connected to Neo4j successfully.")
        except Exception as e:
            self.connected = False
            logger.error(f"Neo4j connection failed: {e}")

    async def close(self):
        if self.driver:
            await self.driver.close()

Neo4jDriver = Neo4jConnection()
