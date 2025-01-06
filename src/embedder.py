import google.generativeai as genai
import numpy as np
from typing import List

class GeminiEmbedder:
    def __init__(self):
        # Initialize the embedding model
        self.model = 'models/embedding-001'
        
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Get embeddings for a list of texts
        """
        try:
            embeddings = []
            for text in texts:
                embedding = genai.embed_content(
                    model=self.model,
                    content=text,
                    task_type="retrieval_document"
                )
                embeddings.append(embedding['embedding'])
            return embeddings
        except Exception as e:
            print(f"Error getting embeddings: {e}")
            return []
            
    def compute_similarity(self, query_embedding: List[float], doc_embeddings: List[List[float]]) -> List[float]:
        """
        Compute cosine similarity between query and documents
        """
        similarities = []
        query_norm = np.linalg.norm(query_embedding)
        
        for doc_embedding in doc_embeddings:
            doc_norm = np.linalg.norm(doc_embedding)
            dot_product = np.dot(query_embedding, doc_embedding)
            similarity = dot_product / (query_norm * doc_norm)
            similarities.append(similarity)
            
        return similarities 