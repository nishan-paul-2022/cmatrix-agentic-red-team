"""LLM API endpoints for configuration profile management - Simplified."""

import json

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.llm import (
    ConfigurationProfile,
    ConfigurationProfileSchema,
    CreateProfileRequest,
    FetchModelsRequest,
    FetchModelsResponse,
    UpdateProfileRequest,
)
from app.models.user import User
from app.services.llm.api_provider_service import api_provider_service
from app.services.llm.config_profile_service import config_profile_service

router = APIRouter()


@router.get("/profiles", response_model=list[ConfigurationProfileSchema])
async def get_profiles(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    """Get all configuration profiles for the current user."""
    try:
        profiles = await config_profile_service.get_user_profiles(db, current_user.id)

        # Convert to schema with masked API keys
        result = []
        for profile in profiles:
            # Mask API key
            key = profile.api_key
            masked_key = f"{key[:4]}...{key[-4:]}" if len(key) > 8 else "***"

            result.append(
                ConfigurationProfileSchema(
                    id=profile.id,
                    user_id=profile.user_id,
                    name=profile.name,
                    api_provider=profile.api_provider,
                    api_key_masked=masked_key,
                    selected_model_name=profile.selected_model_name,
                    is_active=profile.is_active,
                )
            )

        return result
    except Exception as e:
        logger.error(f"Failed to fetch profiles: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/profiles", response_model=ConfigurationProfileSchema)
async def create_profile(
    request: CreateProfileRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new configuration profile."""
    try:
        profile = await config_profile_service.create_profile(
            db,
            current_user.id,
            request.name,
            request.api_provider,
            request.api_key,
            request.selected_model_name,
        )

        # Mask API key
        key = profile.api_key
        masked_key = f"{key[:4]}...{key[-4:]}" if len(key) > 8 else "***"

        return ConfigurationProfileSchema(
            id=profile.id,
            user_id=profile.user_id,
            name=profile.name,
            api_provider=profile.api_provider,
            api_key_masked=masked_key,
            selected_model_name=profile.selected_model_name,
            is_active=profile.is_active,
        )
    except Exception as e:
        logger.error(f"Failed to create profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/profiles/{profile_id}", response_model=ConfigurationProfileSchema)
async def update_profile(
    profile_id: int,
    request: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update a configuration profile."""
    try:
        profile = await config_profile_service.update_profile(
            db,
            profile_id,
            current_user.id,
            request.name,
            request.api_provider,
            request.api_key,
            request.selected_model_name,
        )

        # Mask API key
        key = profile.api_key
        masked_key = f"{key[:4]}...{key[-4:]}" if len(key) > 8 else "***"

        return ConfigurationProfileSchema(
            id=profile.id,
            user_id=profile.user_id,
            name=profile.name,
            api_provider=profile.api_provider,
            api_key_masked=masked_key,
            selected_model_name=profile.selected_model_name,
            is_active=profile.is_active,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to update profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/profiles/{profile_id}")
async def delete_profile(
    profile_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a configuration profile."""
    try:
        await config_profile_service.delete_profile(db, profile_id, current_user.id)
        return {"message": "Profile deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to delete profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/profiles/{profile_id}/activate")
async def activate_profile(
    profile_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Activate a configuration profile."""
    try:
        profile = await config_profile_service.activate_profile(db, profile_id, current_user.id)
        return {"message": "Profile activated successfully", "profile_id": profile.id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to activate profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/providers")
async def get_providers():
    """Get list of supported API providers."""
    return {
        "providers": [
            {"id": "Cerebras", "name": "Cerebras"},
            {"id": "Gemini", "name": "Gemini"},
            {"id": "Hugging Face", "name": "Hugging Face"},
            {"id": "Openrouter", "name": "Openrouter"},
        ]
    }


@router.post("/providers/fetch-models", response_model=FetchModelsResponse)
async def fetch_models(request: FetchModelsRequest, current_user: User = Depends(get_current_user)):
    """Fetch available models from a provider."""
    try:
        models = await api_provider_service.fetch_models(request.api_provider, request.api_key)
        return FetchModelsResponse(provider=request.api_provider, models=models)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to fetch models: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch models: {str(e)}")


@router.get("/profiles/{profile_id}/models", response_model=FetchModelsResponse)
async def fetch_profile_models(
    profile_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Fetch available models for a specific configuration profile."""
    try:
        # Get profile to retrieve API key
        result = await db.execute(
            select(ConfigurationProfile).where(
                ConfigurationProfile.id == profile_id,
                ConfigurationProfile.user_id == current_user.id,
            )
        )
        profile = result.scalar_one_or_none()

        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        models = await api_provider_service.fetch_models(profile.api_provider, profile.api_key)

        return FetchModelsResponse(provider=profile.api_provider, models=models)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to fetch models for profile {profile_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/config/import")
async def import_config(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Import configuration from JSON file."""
    try:
        content = await file.read()
        config_data = json.loads(content.decode("utf-8"))

        if "profiles" not in config_data:
            raise HTTPException(status_code=400, detail="Invalid JSON: missing 'profiles' key")

        imported_count = 0
        for profile_data in config_data["profiles"]:
            # Create profile
            profile = await config_profile_service.create_profile(
                db,
                current_user.id,
                profile_data["name"],
                profile_data["api_provider"],
                profile_data["api_key"],
                profile_data.get("selected_model_name"),
            )

            # Activate if specified
            if profile_data.get("is_active"):
                await config_profile_service.activate_profile(db, profile.id, current_user.id)

            imported_count += 1

        return {"message": f"Successfully imported {imported_count} profiles"}
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        logger.error(f"Failed to import config: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/config/export")
async def export_config(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    """Export configuration to JSON."""
    try:
        profiles = await config_profile_service.get_user_profiles(db, current_user.id)

        export_data = {"profiles": []}
        for profile in profiles:
            export_data["profiles"].append(
                {
                    "name": profile.name,
                    "api_provider": profile.api_provider,
                    "api_key": profile.api_key,
                    "selected_model_name": profile.selected_model_name,
                    "is_active": profile.is_active,
                }
            )

        return JSONResponse(content=export_data)
    except Exception as e:
        logger.error(f"Failed to export config: {e}")
        raise HTTPException(status_code=500, detail=str(e))
