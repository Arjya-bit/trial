"""
Elasticsearch Client Configuration
"""
from elasticsearch import AsyncElasticsearch
from typing import Optional, Dict, Any, List
from datetime import datetime
from ..core.config import settings

es_client: Optional[AsyncElasticsearch] = None


async def init_elasticsearch():
    """Initialize Elasticsearch connection"""
    global es_client
    es_client = AsyncElasticsearch(
        [settings.ELASTICSEARCH_URL],
        verify_certs=False,
        max_retries=3,
        retry_on_timeout=True
    )
    
    # Create indices if they don't exist
    await create_indices()
    print("✅ Elasticsearch connected")


async def close_elasticsearch():
    """Close Elasticsearch connection"""
    global es_client
    if es_client:
        await es_client.close()
        print("✅ Elasticsearch disconnected")


async def get_elasticsearch() -> AsyncElasticsearch:
    """Get Elasticsearch client"""
    return es_client


async def create_indices():
    """Create required indices"""
    indices = [
        "forensics-logs",
        "network-traffic",
        "ot-security-events",
        "system-logs",
        "c2-communications",
        "alerts"
    ]
    
    for index in indices:
        if not await es_client.indices.exists(index=index):
            await es_client.indices.create(
                index=index,
                body={
                    "settings": {
                        "number_of_shards": 2,
                        "number_of_replicas": 1
                    },
                    "mappings": {
                        "properties": {
                            "timestamp": {"type": "date"},
                            "severity": {"type": "keyword"},
                            "source": {"type": "keyword"},
                            "message": {"type": "text"},
                            "data": {"type": "object"}
                        }
                    }
                }
            )


async def index_document(index: str, document: Dict[Any, Any]) -> str:
    """Index a document"""
    if not document.get("timestamp"):
        document["timestamp"] = datetime.utcnow().isoformat()
    
    result = await es_client.index(index=index, document=document)
    return result["_id"]


async def search_documents(index: str, query: Dict[Any, Any], size: int = 100) -> List[Dict]:
    """Search documents"""
    result = await es_client.search(index=index, body=query, size=size)
    return [hit["_source"] for hit in result["hits"]["hits"]]


async def bulk_index(index: str, documents: List[Dict[Any, Any]]):
    """Bulk index documents"""
    from elasticsearch.helpers import async_bulk
    
    actions = [
        {
            "_index": index,
            "_source": doc
        }
        for doc in documents
    ]
    
    await async_bulk(es_client, actions)
