import pathway as pw
from pathway.stdlib.ml.index import KNNIndex
from typing import List, Dict
import pypdf
import os

class DocumentProcessor:
    def __init__(self):
        self.supported_formats = {'.txt', '.pdf'}
        
    def process_document(self, file_path: str) -> List[Dict]:
        """Process documents into chunks with metadata"""
        ext = os.path.splitext(file_path)[1]
        if ext not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {ext}")
            
        if ext == '.pdf':
            return self._process_pdf(file_path)
        return self._process_txt(file_path)
    
    def _process_pdf(self, file_path: str) -> List[Dict]:
        chunks = []
        with open(file_path, 'rb') as file:
            pdf = pypdf.PdfReader(file)
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                # Create chunks of approximately 1000 characters
                for j, chunk in enumerate(self._chunk_text(text)):
                    chunks.append({
                        'content': chunk,
                        'metadata': {
                            'source': file_path,
                            'page': i + 1,
                            'chunk': j + 1
                        }
                    })
        return chunks
    
    def _process_txt(self, file_path: str) -> List[Dict]:
        chunks = []
        with open(file_path, 'r') as file:
            text = file.read()
            for i, chunk in enumerate(self._chunk_text(text)):
                chunks.append({
                    'content': chunk,
                    'metadata': {
                        'source': file_path,
                        'chunk': i + 1
                    }
                })
        return chunks
    
    def _chunk_text(self, text: str, chunk_size: int = 1000) -> List[str]:
        """Split text into chunks of approximately chunk_size characters"""
        words = text.split()
        chunks = []
        current_chunk = []
        current_size = 0
        
        for word in words:
            word_size = len(word) + 1  # +1 for space
            if current_size + word_size > chunk_size and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_size = word_size
            else:
                current_chunk.append(word)
                current_size += word_size
                
        if current_chunk:
            chunks.append(' '.join(current_chunk))
            
        return chunks 