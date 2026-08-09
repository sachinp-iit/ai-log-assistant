# services/retrieval_service.py

from langchain_huggingface import HuggingFaceEmbeddings
from FlagEmbedding import FlagReranker
from qdrant_client import QdrantClient, models

from config.settings import settings
from core.logger import logger

# ==========================================================
# RETRIEVAL SERVICE
# ==========================================================

class RetrievalService:
    """
    Handles semantic retrieval of infrastructure logs from Qdrant vector database
    """
    
    def __init__(self):
        # Initialize Qdrant client
        self.client = QdrantClient(
            host = settings.QDRANT_HOST,
            port = settings.QDRANT_PORT
        )
        
        # Initialize the same embedding model used during Ingestion Service
        self.embedding_model = HuggingFaceEmbeddings (
            model_name = settings.EMBEDDING_MODEL,
            model_kwargs = {"device": "cpu"},
            encode_kwargs = {"normalize_embeddings": True}
        )
        
        # Initialize BGE reranker
        self.reranker = FlagReranker(
            settings.RERANKER_MODEL,
            use_fp16 = False,
        )
        
        logger.info("Retrieval service initialized.")
        
    
    def embed_query(self, query: str) -> list[float]:
        """
        Convert the user's query into an embedding vector.
        """
        
        return self.embedding_model.embed_query(query)
    
    
    def rerank(self, query: str, results: list[dict]) -> list[dict]:
        """
        Rerank retrieved documents using the BGE reranker
        """
        
        if not results:
            return []
        
        pairs = [
            [query, result["content"]]
            for result in results
        ]
        
        scores = self.reranker.compute_score(
            pairs,
            normalize = True,
        )
        
        if not isinstance(scores, list):
            scores = [scores]
            
        for result, score in zip(results, scores):
            result["rerank_score"] = float(score)
            
        return sorted(
            results,
            key = lambda result: result["rerank_score"],
            reverse = True
        )    
    
    
    def search(self, query: str, filters: dict | None = None, limit: int | None = None) -> list[dict]:
        """
        Perform semantic similarity search with optional metadata filters and rerank the retrieved results.
        """
        
        query_vector = self.embed_query(query)
        query_filter = None
        
        if filters:
            query_filter = models.Filter(
                must = [
                    models.FieldCondition(
                        key = key,
                        match = models.MatchValue(value = value),
                    )
                    for key, value in filters.items()
                ]
            )
        
        
        result = self.client.query_points(
            collection_name=settings.QDRANT_COLLECTION,
            query = query_vector,
            query_filter = query_filter,
            limit = limit or settings.TOP_K_RESULTS, # Retrieve matching Top N records
            with_payload = True,
        )
        
        documents = [
            {
                "score": point.score,
                "content": point.payload.get("page_content"),
                "metadata": {
                    key: value
                    for key, value in point.payload.items()
                    if key != "page_content"
                },
            }
            for point in result.points
        ]
        
        return self.rerank(
            query = query,
            results = documents,
        )
        
        
        
    
    