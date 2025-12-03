#!/usr/bin/env python3
"""
Warmup script to pre-load embedding and reranker models.
Run this after deployment to avoid slow first requests.
"""

import sys

sys.path.insert(0, "/app")

from loguru import logger


def warmup_models():
    """Pre-load all models to avoid slow first requests."""
    logger.info("🔥 Warming up models...")
    logger.info("=" * 60)

    # Warmup embedding model
    logger.info("\n1️⃣  Pre-loading BGE-large embedding model...")
    try:
        from app.services.vector_store import get_vector_store

        store = get_vector_store()
        store._setup_model()

        if store._model:
            logger.info("   ✅ Embedding model loaded and cached")
            logger.info(f"   Model: {store._model}")

            # Test embedding
            test_embedding = store._model.encode("test warmup")
            logger.info(f"   ✅ Test embedding generated ({len(test_embedding)} dimensions)")
        else:
            logger.error("   ❌ Failed to load embedding model")
            return False
    except Exception as e:
        logger.error(f"   ❌ Error: {e}")
        return False

    # Warmup reranker (optional, takes longer)
    logger.info("\n2️⃣  Pre-loading BGE-reranker model (optional)...")
    try:
        store._setup_reranker()

        if store._reranker:
            logger.info("   ✅ Reranker model loaded and cached")
            logger.info("   Model: BAAI/bge-reranker-large")

            # Test reranking
            store._reranker.predict([["query", "document"]])
            logger.info("   ✅ Test reranking completed")
        else:
            logger.warning("   ⚠️  Reranker not loaded (will load on first use)")
    except Exception as e:
        logger.warning(f"   ⚠️  Reranker warmup skipped: {e}")

    logger.info("\n" + "=" * 60)
    logger.info("✅ Warmup complete!")
    logger.info("\n📊 Summary:")
    logger.info("   ✅ Embedding model: Loaded and cached in memory")
    logger.info("   ✅ Future requests: Will be fast (~1-2 seconds)")
    logger.info("\n🚀 System ready for production use!")

    return True


if __name__ == "__main__":
    success = warmup_models()
    sys.exit(0 if success else 1)
