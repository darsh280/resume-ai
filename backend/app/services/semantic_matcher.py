"""
Semantic Matcher Service
========================
Uses the SentenceTransformers library with the 'all-MiniLM-L6-v2' model
to compute dense sentence embeddings and cosine similarity between a job
description and a candidate resume.

Why all-MiniLM-L6-v2?
  - Small (22M params) and fast — suitable for local inference.
  - High quality semantic representations for English text.
  - Maps sentences to a 384-dimensional embedding space.

The model is loaded once at module level and reused across requests.
"""

from typing import List
import numpy as np

try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity as sk_cosine
    _TRANSFORMERS_AVAILABLE = True
except ImportError:
    _TRANSFORMERS_AVAILABLE = False


# ---------------------------------------------------------------------------
# Singleton model loader
# ---------------------------------------------------------------------------
_model: "SentenceTransformer | None" = None


def _get_model():
    """Load the SentenceTransformer model once and cache it."""
    global _model
    if _model is None:
        if not _TRANSFORMERS_AVAILABLE:
            raise ImportError(
                "sentence-transformers is not installed. "
                "Run: pip install sentence-transformers"
            )
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


# ---------------------------------------------------------------------------
# Main service
# ---------------------------------------------------------------------------

class SemanticMatcher:
    """Compute semantic similarity between job descriptions and resumes."""

    # Maximum characters sent to the model (≈ 512 tokens at ~4 chars/token)
    _MAX_CHARS = 2000

    def compute_similarity(self, jd_text: str, resume_text: str) -> float:
        """
        Returns cosine similarity score in [0.0, 1.0].

        Steps:
          1. Truncate texts to avoid exceeding the model's token limit.
          2. Encode both texts into embeddings via the transformer.
          3. Compute cosine similarity between the two embedding vectors.
        """
        if not jd_text or not resume_text:
            return 0.0

        jd_trunc = jd_text[: self._MAX_CHARS]
        resume_trunc = resume_text[: self._MAX_CHARS]

        model = _get_model()
        embeddings = model.encode(
            [jd_trunc, resume_trunc],
            convert_to_numpy=True,
            show_progress_bar=False,
        )

        # cosine_similarity returns shape (1, 1) → extract scalar
        sim = sk_cosine(
            embeddings[0].reshape(1, -1),
            embeddings[1].reshape(1, -1),
        )
        return float(np.clip(sim[0][0], 0.0, 1.0))

    def batch_similarity(self, jd_text: str, resume_texts: List[str]) -> List[float]:
        """
        Efficiently compute similarity between one JD and many resumes.
        Encodes all texts in a single forward pass.
        """
        if not resume_texts:
            return []

        jd_trunc = jd_text[: self._MAX_CHARS]
        resume_trunc = [t[: self._MAX_CHARS] for t in resume_texts]

        model = _get_model()
        all_texts = [jd_trunc] + resume_trunc
        embeddings = model.encode(
            all_texts,
            convert_to_numpy=True,
            show_progress_bar=False,
        )

        jd_emb = embeddings[0].reshape(1, -1)
        resume_embs = embeddings[1:]

        similarities = sk_cosine(jd_emb, resume_embs)[0]
        return [float(np.clip(s, 0.0, 1.0)) for s in similarities]
