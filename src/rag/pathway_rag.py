import pathway as pw
from pathway.xpacks.llm.embedders import OpenAIEmbedder
from pathway.xpacks.llm.splitters import TokenSplitter
from pathway.xpacks.llm import prompts
import os
from typing import Dict

class PathwayHealthRAG:
    def __init__(self):
        self.context = pw.Context()
        self.embedder = OpenAIEmbedder(api_key=os.getenv("OPENAI_API_KEY"))
        self.splitter = TokenSplitter(chunk_size=500)
        
        # Load health guidelines into knowledge base
        self.knowledge_base = self._load_knowledge_base()
        
    def _load_knowledge_base(self):
        """Load and index health guidelines"""
        # Create input table from health guidelines
        guidelines = pw.io.csv.read("data/health_guidelines.csv")
        
        # Process and embed documents
        documents = guidelines.select(
            text=pw.this.content,
            metadata=pw.this.category
        )
        
        chunks = documents.flat_map(
            lambda x: self.splitter.split(x["text"]),
            schema=documents.schema
        )
        
        return chunks.select(
            embedding=self.embedder.embed(pw.this.text),
            text=pw.this.text,
            metadata=pw.this.metadata
        )
    
    def get_recommendation(self, query: str, health_data: Dict) -> str:
        """Generate recommendations using RAG"""
        # Embed query
        query_embedding = self.embedder.embed(query)
        
        # Retrieve relevant context
        relevant_chunks = self.knowledge_base.select(
            score=pw.cosine_similarity(query_embedding, pw.this.embedding)
        ).sort(pw.this.score, reverse=True).limit(3)
        
        # Format prompt with context and health data
        prompt = prompts.QA_PROMPT.format(
            context="\n".join(relevant_chunks.collect()["text"]),
            query=query,
            health_data=health_data
        )
        
        # Generate response
        response = pw.llm.generate(prompt)
        
        return response.text 