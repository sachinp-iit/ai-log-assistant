# services/ingestion_service.py

from pathlib import Path
import pandas as pd
from core.logger import logger
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.settings import settings


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