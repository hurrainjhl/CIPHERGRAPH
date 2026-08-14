import json
import logging
from openai import AsyncOpenAI
from config.settings import settings

logger = logging.getLogger("ciphergraph")

client = AsyncOpenAI(
    api_key=settings.openai_api_key,
    base_url=settings.openai_base_url
)

EXTRACTION_PROMPT = """You are an elite Cyber Threat Intelligence analyst.
Extract entities and relationships from the provided CTI report.

ENTITIES:
Identify threat actors, malware, IPs, domains, vulnerabilities, and victims.
IMPORTANT: You must strictly categorize every entity into one of the following exact types:
- Attacker (e.g. APT28, Lazarus, Threat Actors)
- Indicator (e.g. 192.168.1.1, malware.com, MD5 hash, CVE-2021-1234)
- Victim (e.g. Government, Finance Sector, specific companies)
- Tool (e.g. Cobalt Strike, Mimikatz, custom malware families)

RELATIONSHIPS:
Identify how these entities interact. Use clear verbs (e.g. TARGETS, USES, COMMUNICATES_WITH, EXPLOITS).

Return valid JSON exactly in this format:
{
  "entities": [
    {"name": "string", "type": "string (Attacker|Indicator|Victim|Tool)", "summary": "string description"}
  ],
  "relationships": [
    {"source": "entity_name", "target": "entity_name", "type": "string", "fact": "string context"}
  ]
}
"""

async def extract_entities(text: str) -> dict:
    try:
        response = await client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {"role": "system", "content": EXTRACTION_PROMPT},
                {"role": "user", "content": f"Extract intelligence from this report:\n\n{text}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        logger.error(f"LLM Extraction failed: {e}")
        return {"entities": [], "relationships": []}
