from typing import List, Dict, Optional
import numpy as np
from pathlib import Path
import pickle
import os

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    print("FAISS not available. Vector search will be disabled.")


class VectorStore:
    """Vector database for semantic search of logs, incidents, and runbooks"""

    def __init__(self, dimension: int = 384, index_path: str = "./faiss_index"):
        self.dimension = dimension
        self.index_path = Path(index_path)
        self.index_path.mkdir(exist_ok=True)

        # Initialize FAISS index
        if FAISS_AVAILABLE:
            self.index = faiss.IndexFlatL2(dimension)
        else:
            self.index = None

        # Store metadata for each vector
        self.metadata: List[Dict] = []

        # Load existing index if available
        self.load()

    def add_vectors(self, vectors: np.ndarray, metadata: List[Dict]):
        """Add vectors with metadata to the index"""
        if not FAISS_AVAILABLE or self.index is None:
            return

        # Ensure vectors are float32
        vectors = vectors.astype('float32')

        # Normalize vectors for cosine similarity
        faiss.normalize_L2(vectors)

        # Add to index
        self.index.add(vectors)
        self.metadata.extend(metadata)

    def search(self, query_vector: np.ndarray, k: int = 5) -> List[Dict]:
        """Search for similar vectors"""
        if not FAISS_AVAILABLE or self.index is None:
            return []

        # Ensure query is float32 and normalized
        query_vector = query_vector.astype('float32').reshape(1, -1)
        faiss.normalize_L2(query_vector)

        # Search
        distances, indices = self.index.search(query_vector, k)

        # Return results with metadata
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.metadata):
                result = self.metadata[idx].copy()
                result['distance'] = float(distances[0][i])
                result['similarity'] = 1.0 / (1.0 + result['distance'])
                results.append(result)

        return results

    def save(self):
        """Save index and metadata to disk"""
        if not FAISS_AVAILABLE or self.index is None:
            return

        # Save FAISS index
        index_file = self.index_path / "index.faiss"
        faiss.write_index(self.index, str(index_file))

        # Save metadata
        metadata_file = self.index_path / "metadata.pkl"
        with open(metadata_file, 'wb') as f:
            pickle.dump(self.metadata, f)

    def load(self):
        """Load index and metadata from disk"""
        if not FAISS_AVAILABLE:
            return

        index_file = self.index_path / "index.faiss"
        metadata_file = self.index_path / "metadata.pkl"

        if index_file.exists() and metadata_file.exists():
            try:
                # Load FAISS index
                self.index = faiss.read_index(str(index_file))

                # Load metadata
                with open(metadata_file, 'rb') as f:
                    self.metadata = pickle.load(f)

                print(f"Loaded vector store with {len(self.metadata)} entries")
            except Exception as e:
                print(f"Error loading vector store: {e}")

    def clear(self):
        """Clear all data from the index"""
        if FAISS_AVAILABLE:
            self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata = []


# Global vector store instance
vector_store = VectorStore()
