"""NVD CVE Sync Script - Automated CVE ingestion from NVD feeds.

This script downloads and processes CVE data from the National Vulnerability Database (NVD)
and stores it in the CVE Vector Store for semantic search.

Features:
- Full sync: Download all CVEs from NVD
- Incremental sync: Download only recent CVEs (last N days)
- Batch processing for efficiency
- Progress tracking and error handling
- Automatic retry on failures

Usage:
    # Full sync (WARNING: Takes hours, downloads 200k+ CVEs)
    python scripts/sync_nvd.py --full

    # Incremental sync (last 7 days)
    python scripts/sync_nvd.py --days 7

    # Incremental sync (last 30 days)
    python scripts/sync_nvd.py --days 30

    # Test mode (only 100 CVEs)
    python scripts/sync_nvd.py --test
"""

import argparse
import asyncio
import os
import sys

from loguru import logger

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.rag.cve_vector_store import get_cve_vector_store
from app.services.rag.nvd_sync_service import NVDSyncService


async def main():
    """Main entry point for NVD sync script."""
    parser = argparse.ArgumentParser(description="Sync CVE data from NVD to vector store")
    parser.add_argument(
        "--full", action="store_true", help="Perform full sync (WARNING: Takes hours)"
    )
    parser.add_argument(
        "--days", type=int, default=7, help="Days to look back for incremental sync"
    )
    parser.add_argument("--test", action="store_true", help="Test mode (only 100 CVEs)")
    parser.add_argument("--api-key", type=str, help="NVD API key for higher rate limits")

    args = parser.parse_args()

    # Initialize vector store
    logger.info("Initializing CVE vector store...")
    vector_store = get_cve_vector_store()

    if not await vector_store.initialize():
        logger.error("❌ Failed to initialize vector store")
        return 1

    # Get initial stats
    stats = await vector_store.get_stats()
    logger.info(f"Current CVE count: {stats.get('total_cves', 0)}")

    # Initialize sync service
    sync_service = NVDSyncService(api_key=args.api_key)

    # Perform sync
    if args.test:
        logger.info("🧪 Running in TEST mode (100 CVEs)")
        total = await sync_service.sync_full(vector_store, max_cves=100)
    elif args.full:
        logger.warning("⚠️  Full sync will take several hours and download 200k+ CVEs")
        logger.warning("Press Ctrl+C within 5 seconds to cancel...")
        try:
            await asyncio.sleep(5)
        except KeyboardInterrupt:
            logger.info("Cancelled by user")
            return 0
        total = await sync_service.sync_full(vector_store)
    else:
        total = await sync_service.sync_incremental(vector_store, days=args.days)

    # Get final stats
    stats = await vector_store.get_stats()
    logger.info(f"Final CVE count: {stats.get('total_cves', 0)}")
    logger.info(f"✅ Sync complete! Processed {total} CVEs")

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
