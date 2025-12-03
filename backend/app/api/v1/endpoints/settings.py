"""API endpoints for system settings management."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from pydantic import BaseModel
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.system_settings import SystemSetting
from app.models.user import User

router = APIRouter()


class SettingResponse(BaseModel):
    key: str
    value: Optional[str]
    description: Optional[str]


class SettingUpdate(BaseModel):
    value: Optional[str]
    description: Optional[str] = None


@router.get("/nvd-api-key", response_model=SettingResponse)
async def get_nvd_api_key(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    """
    Get the NVD API key from database.
    Returns masked value for security.
    """
    result = await db.execute(select(SystemSetting).where(SystemSetting.key == "nvd_api_key"))
    setting = result.scalar_one_or_none()

    if not setting:
        return SettingResponse(
            key="nvd_api_key", value=None, description="NVD API key for CVE synchronization"
        )

    # Mask the API key for security (show only last 4 characters)
    masked_value = None
    if setting.value:
        masked_value = f"****{setting.value[-4:]}" if len(setting.value) > 4 else "****"

    return SettingResponse(key=setting.key, value=masked_value, description=setting.description)


@router.put("/nvd-api-key")
async def update_nvd_api_key(
    update_data: SettingUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Update the NVD API key in database.
    """
    try:
        # Check if setting exists
        result = await db.execute(select(SystemSetting).where(SystemSetting.key == "nvd_api_key"))
        existing = result.scalar_one_or_none()

        if existing:
            # Update existing
            await db.execute(
                update(SystemSetting)
                .where(SystemSetting.key == "nvd_api_key")
                .values(
                    value=update_data.value,
                    description=update_data.description or existing.description,
                )
            )
        else:
            # Create new
            new_setting = SystemSetting(
                key="nvd_api_key",
                value=update_data.value,
                description=update_data.description or "NVD API key for CVE synchronization",
            )
            db.add(new_setting)

        await db.commit()

        logger.info(f"NVD API key updated by user {current_user.id}")

        return {"message": "NVD API key updated successfully"}

    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to update NVD API key: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/nvd-api-key")
async def delete_nvd_api_key(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    """
    Delete the NVD API key from database.
    """
    try:
        await db.execute(delete(SystemSetting).where(SystemSetting.key == "nvd_api_key"))
        await db.commit()

        logger.info(f"NVD API key deleted by user {current_user.id}")

        return {"message": "NVD API key deleted successfully"}

    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to delete NVD API key: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def get_nvd_api_key_from_db(db: AsyncSession) -> Optional[str]:
    """
    Helper function to get NVD API key from database.
    Used by other services.
    """
    result = await db.execute(select(SystemSetting).where(SystemSetting.key == "nvd_api_key"))
    setting = result.scalar_one_or_none()
    return setting.value if setting else None
