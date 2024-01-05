import os
from qdrant_client import QdrantClient
from qdrant_client.http.api_client import UnexpectedResponse
from qdrant_client.http.models import Distance, VectorParams
from dotenv import load_dotenv


load_dotenv()

QDRANT_API_URL = os.environ['QDRANT_API_URL']
QDRANT_API_KEY = os.environ['QDRANT_API_KEY']


def get_qdrant_client() -> QdrantClient:
    qdrant_client = QdrantClient(
        url=QDRANT_API_URL, 
        api_key=QDRANT_API_KEY,
    )

    return qdrant_client

def init_collection(
    qdrant_client: QdrantClient,
    collection_name: str,
    vector_size: int,
) -> QdrantClient:
    try: 
        qdrant_client.get_collection(collection_name=collection_name)

    except (UnexpectedResponse, ValueError):
        qdrant_client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
    )

    return qdrant_client