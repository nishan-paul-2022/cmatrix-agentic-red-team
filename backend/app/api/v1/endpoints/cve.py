from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from loguru import logger
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.services.llm.db_factory import get_db_provider_factory
from app.services.rag.cve_search import get_smart_cve_search_service

router = APIRouter()


class CVESearchResponse(BaseModel):
    query: str
    original_query: str
    results: Optional[dict[str, Any]]
    history: list[str]
    feedback: Optional[str]
    is_corrected: bool


@router.get("/search", response_model=CVESearchResponse)
async def search_cve(
    query: str,
    limit: int = 10,
    strategy: str = "balanced",
    min_cvss_score: Optional[float] = Query(
        None, ge=0.0, le=10.0, description="Minimum CVSS score (0-10)"
    ),
    severity: Optional[str] = Query(
        None, regex="^(LOW|MEDIUM|HIGH|CRITICAL)$", description="Severity level"
    ),
    exploit_available: Optional[bool] = Query(None, description="Filter by exploit availability"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Search for CVEs using the Smart CVE Search tool with vector store.

    Supports semantic search with advanced filtering:
    - min_cvss_score: Filter by minimum CVSS score
    - severity: Filter by severity (LOW, MEDIUM, HIGH, CRITICAL)
    - exploit_available: Filter by exploit availability

    Returns structured data including reranking details and correction history.
    """
    try:
        # Get LLM provider for the current user
        logger.debug("Getting DB provider factory")
        factory = get_db_provider_factory()
        logger.debug(f"Getting active provider for user {current_user.id}")
        llm_provider = await factory.get_active_provider(db, current_user.id)

        if not llm_provider:
            logger.warning("No LLM provider found")
            raise HTTPException(status_code=400, detail="No LLM provider configured")

        logger.debug(f"Got provider: {llm_provider}")
        service = get_smart_cve_search_service(llm_provider)
        logger.debug(f"Calling search service with query='{query}'")
        result = await service.search(
            query=query,
            limit=limit,
            strategy=strategy,
            min_cvss_score=min_cvss_score,
            severity=severity,
            exploit_available=exploit_available,
        )
        logger.debug("Search completed successfully")

        # Convert RerankingResult to dict if present
        if result.get("results"):
            result["results"] = result["results"].to_dict()

        return CVESearchResponse(**result)
    except Exception as e:
        logger.exception(f"Error in CVE search: {e}")
        raise HTTPException(status_code=500, detail=str(e))


from fastapi import BackgroundTasks

from app.services.rag.cve_vector_store import get_cve_vector_store
from app.services.rag.nvd_sync_service import NVDSyncService


class SyncResponse(BaseModel):
    message: str
    task_id: str


async def run_sync_task(full: bool, days: int, api_key: Optional[str]):
    """Background task to run NVD sync."""
    try:
        logger.info(f"Starting background NVD sync (full={full}, days={days})")
        vector_store = get_cve_vector_store()
        await vector_store.initialize()

        sync_service = NVDSyncService(api_key=api_key)

        if full:
            await sync_service.sync_full(vector_store)
        else:
            await sync_service.sync_incremental(vector_store, days=days)

        logger.info("Background NVD sync completed successfully")
    except Exception as e:
        logger.exception(f"Background NVD sync failed: {e}")


from app.api.v1.endpoints.settings import get_nvd_api_key_from_db
from app.core.config import settings


@router.post("/sync", response_model=SyncResponse)
async def sync_cves(
    background_tasks: BackgroundTasks,
    full: bool = False,
    days: int = 7,
    api_key: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Trigger NVD CVE synchronization.

    - **full**: If true, performs a full sync (takes hours).
    - **days**: Number of days to look back for incremental sync (default: 7).
    - **api_key**: Optional NVD API key for higher rate limits.
    """
    # Priority: 1. Provided api_key, 2. Database, 3. Config file
    if not api_key:
        api_key = await get_nvd_api_key_from_db(db)
    if not api_key:
        api_key = settings.NVD_API_KEY

    task_id = f"sync_{'full' if full else 'inc'}_{days}d"
    background_tasks.add_task(run_sync_task, full, days, api_key)

    return SyncResponse(
        message=f"CVE sync started in background ({'Full' if full else 'Incremental'}, {days} days)",
        task_id=task_id,
    )
