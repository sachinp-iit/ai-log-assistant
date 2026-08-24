# services/ingestion_service.py

from pathlib import Path
import pandas as pd
from core.logger import logger
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.settings import settings
from langchain_huggingface import HuggingFaceEmbeddings

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from concurrent.futures import ThreadPoolExecutor

# ==========================================================
# INGESTION SERVICE
# ==========================================================

class IngestionService:
    
    def __init__(self, dataset_path: str):
        self.dataset_path = Path(dataset_path)
        
    def load_logs(self) -> pd.DataFrame:
        
        logger.info(f"Loading dataset: {self.dataset_path}")
        dataframe = pd.read_csv(self.dataset_path)
        logger.info(f"Loaded {len(dataframe)} records.")
        
        return dataframe
    
    def validate_dataset(self, dataframe: pd.DataFrame) -> None:
        
        if dataframe.empty:
            raise ValueError("Dataset is empty.")
        
        logger.info("Dataset validation completed.")
        
    def preprocess_dataset(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        
        dataframe = dataframe.drop_duplicates()
        dataframe = dataframe.fillna("Unknown")
        
        logger.info("Dataset preprocessing completed.")
        
        return dataframe
    
    def create_documents(self, dataframe: pd.DataFrame) -> list[Document]:
        
        documents = []
        
        for index, row in dataframe.iterrows():
            
            page_content = "\n".join(
                f"{column}: {value}"
                for column, value in row.items()
            )
            
            documents.append(
                Document(
                    id = str(index),
                    page_content = page_content,
                    metadata = row.to_dict(),
                )
            )

        logger.info(f"Created {len(documents)} LangChain documents.")
        
        return documents
    
    def chunk_documents(self, documents: list[Document]) -> list[Document]:
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )
        
        chunks = text_splitter.split_documents(documents)
        
        logger.info(f"Created {len(chunks)} document chunks.")
        
        return chunks
    
    def get_embedding_model(self) -> HuggingFaceEmbeddings:
            
        logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
        
        return HuggingFaceEmbeddings(
            model_name = settings.EMBEDDING_MODEL,
            model_kwargs = {"device": "cpu"},
            encode_kwargs = {"normalize_embeddings": True}
        )
    
    def generate_embeddings(self, chunks: list[Document]) -> list[Document]:
        
        embeddings = self.get_embedding_model()     
       
        # Validate the embedding model before Qdrant ingestion.
        if not chunks:
            raise ValueError("No document chunks available.")
        
        embeddings.embed_documents(
            [chunk.page_content for chunk in chunks[:1]]
        )
        
        logger.info(f"Generated embeddings for {len(chunks)} chunks.")
        
        return chunks
    
    def get_qdrant_client(self) -> QdrantClient:
        
        client = QdrantClient(
            host = settings.QDRANT_HOST,
            port = settings.QDRANT_PORT
        )
        
        if not client.collection_exists(settings.QDRANT_COLLECTION):
            client.create_collection(
                collection_name = settings.QDRANT_COLLECTION,
                vectors_config = VectorParams(
                    size = settings.EMBEDDING_DIMENSION,
                    distance = Distance.COSINE
                ),
            )
            
            logger.info(
                f"Created Qdrant collection: "
                f"{settings.QDRANT_COLLECTION}")
            
        
        return client
    
    def ingest_to_qdrant(self, chunks: list[Document], 
                         embeddings: HuggingFaceEmbeddings, client: QdrantClient) -> None:
        
        batch_size = settings.INGESTION_BATCH_SIZE
        
        for start in range(0, len(chunks), batch_size):
            batch = chunks[start: start + batch_size]
            
            vectors = embeddings.embed_documents(
                [document.page_content for document in batch]
            )
            
            points = [
                PointStruct(
                    id = start + 1,
                    vector = vector,
                    payload = {
                        "page_content": document.page_content,
                        **document.metadata
                    },
                )
                for document, vector in zip(batch, vectors)
            ]
            
            client.upsert(
                collection_name = settings.QDRANT_COLLECTION, 
                points = points,
            )
            
            logger.info(
                f"Stored batch {start // batch_size + 1} "
                f"with {len(points)} documents."
            )
            
    
    def ingest_batches(self, chunks: list[Document], embeddings: HuggingFaceEmbeddings,
    client: QdrantClient,) -> None:
        """
        Process document chunks in parallel batches and store them in Qdrant.
        """

        batch_size = settings.INGESTION_BATCH_SIZE

        batches = [
            chunks[i:i + batch_size]
            for i in range(0, len(chunks), batch_size)
        ]

        def process_batch(
            batch_index: int,
            batch: list[Document],
        ) -> None:
            """
            Generate embeddings and store one batch in Qdrant.
            """

            vectors = embeddings.embed_documents(
                [document.page_content for document in batch]
            )

            points = [
                PointStruct(
                    # Every document gets a unique Qdrant ID.
                    id=batch_index * batch_size + i,
                    vector=vector,
                    payload={
                        "page_content": document.page_content,
                        **document.metadata,
                    },
                )
                for i, (document, vector) in enumerate(
                    zip(batch, vectors)
                )
            ]

            client.upsert(
                collection_name=settings.QDRANT_COLLECTION,
                points=points,
            )

            logger.info(
                f"Batch {batch_index + 1}/{len(batches)} "
                f"ingested: {len(points)} points."
            )

        with ThreadPoolExecutor(
            max_workers=settings.MAX_CONCURRENT_BATCHES
        ) as executor:

            futures = [
                executor.submit(
                    process_batch,
                    batch_index,
                    batch,
                )
                for batch_index, batch in enumerate(batches)
            ]

            for future in futures:
                future.result()
                
                
    def run_ingestions(self) -> None:
        
        # Load the data from the infra_logs folder having name as Cloud_Anomaly_Dataset.csv
        dataframe = self.load_logs()
        # Check whether the loaded dataset is having a data in it
        self.validate_dataset(dataframe)
        # Do a data cleansing like removing null, blank data
        dataframe = self.preprocess_dataset(dataframe)
        # Convert the loaded data into langchain document object
        documents = self.create_documents(dataframe)
        # Split the text into chunks with overlap
        chunks = self.chunk_documents(documents)
        # Convert each chunk into embedding/vector
        embeddings = self.get_embedding_model()
        client = self.get_qdrant_client()
        self.ingest_batches(
            chunks=chunks,
            embeddings=embeddings,
            client = client
        )
        
        logger.info("Infrastructure log ingestion completed.")
        