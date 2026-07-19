#!/usr/bin/env python
# =============================================================================
# Rashid Dental AI Assistant — Index Builder Script
# =============================================================================
# CLI entrypoint to build (or rebuild) the FAISS knowledge-base index.
#
# Usage:
#   python scripts/build_index.py              # Live mode (requires GOOGLE_API_KEY)
#   python scripts/build_index.py --mock       # Mock mode (offline, no API key needed)
#   python scripts/build_index.py --force      # Force rebuild even if index is current
#
# Run from project root:
#   venv\Scripts\python scripts/build_index.py --mock
# =============================================================================

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Make sure project root is on the path so backend.* imports work
# ---------------------------------------------------------------------------
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from backend.app.rag.chunker import MarkdownChunker
from backend.app.rag.cleaner import MarkdownCleaner
from backend.app.rag.embedder import Embedder, EmbedderMode
from backend.app.rag.loader import MarkdownLoader
from backend.app.rag.vector_store import VectorStore

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_KB_DIR = _PROJECT_ROOT / "knowledge-base"
_INDEX_PATH = _PROJECT_ROOT / "backend" / "vector_store" / "faiss.index"
_META_PATH = _PROJECT_ROOT / "backend" / "vector_store" / "chunks.pkl"


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Build the FAISS knowledge-base index for Rashid Dental AI Assistant."
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Use mock (random) embeddings — no GOOGLE_API_KEY required.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force rebuild even if index is already up-to-date.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Demo: number of results to show in the test search (default: 5).",
    )
    return parser.parse_args()


def main() -> None:
    """Orchestrate the full index build pipeline."""
    args = parse_args()
    t0 = time.perf_counter()

    mode = EmbedderMode.MOCK if args.mock else EmbedderMode.LIVE
    print(f"\n{'=' * 60}")
    print("  Rashid Dental AI — Index Builder")
    print(f"  Mode       : {'MOCK (offline)' if args.mock else 'LIVE (Google API)'}")
    print(f"  KB dir     : {_KB_DIR}")
    print(f"  Index path : {_INDEX_PATH}")
    print(f"{'=' * 60}\n")

    # Step 1 — Load
    print("Step 1/4  Loading markdown files...")
    loader = MarkdownLoader(_KB_DIR)
    documents = loader.load_all()
    print(f"          Loaded {len(documents)} document(s)\n")

    if not documents:
        print("ERROR: No markdown files found. Check knowledge-base/ directory.")
        sys.exit(1)

    # Step 2 — Clean + Chunk
    print("Step 2/4  Cleaning and chunking documents...")
    cleaner = MarkdownCleaner()
    chunker = MarkdownChunker()

    all_chunks = []
    for doc in documents:
        cleaned = cleaner.clean(doc.content)
        chunks = chunker.chunk(doc.filename, cleaned)
        all_chunks.extend(chunks)
        print(f"          {doc.filename:40s} -> {len(chunks)} chunk(s)")

    print(f"\n          Total chunks: {len(all_chunks)}\n")

    # Step 3 — Embed + Build
    print("Step 3/4  Generating embeddings and building FAISS index...")
    if not args.mock:
        print("          (This calls the Google API - may take a moment)\n")

    from backend.app.core.config import settings

    embedder = Embedder(mode=mode, api_key=settings.gemini_api_key)
    store = VectorStore(index_path=_INDEX_PATH, meta_path=_META_PATH)
    store.build(all_chunks, embedder)

    # Step 4 — Save
    print("\nStep 4/4  Saving index to disk...")
    store.save()
    print(f"          Saved {store.chunk_count} chunk(s)\n")

    elapsed = time.perf_counter() - t0
    print(f"{'=' * 60}")
    print(f"  Build complete in {elapsed:.2f}s")
    print(f"{'=' * 60}\n")

    # Quick sanity search
    print("Quick search test - query: 'What are the clinic opening hours?'")
    print("-" * 60)
    query = "What are the clinic opening hours?"
    query_vec = embedder.embed_query(query)
    results = store.search(query_vec, top_k=args.top_k)

    for rank, (chunk, score) in enumerate(results, 1):
        print(
            f"  [{rank}] score={score:.4f}  file={chunk.filename}  "
            f"heading='{chunk.heading}'  words={chunk.word_count}"
        )
        print(f"      chunk_id={chunk.chunk_id}")
        print()

    print("Index build + verification complete.\n")


if __name__ == "__main__":
    main()
