"""Configuration Profile service layer - Simplified."""

from typing import Optional

from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.llm import ConfigurationProfile


class ConfigProfileService:
    """Service for managing configuration profiles."""

    @staticmethod
    async def create_profile(
        db: AsyncSession,
        user_id: int,
        name: str,
        api_provider: str,
        api_key: str,
        selected_model_name: Optional[str] = None,
    ) -> ConfigurationProfile:
        """Create a new configuration profile."""
        profile = ConfigurationProfile(
            user_id=user_id,
            name=name,
            api_provider=api_provider,
            api_key=api_key,
            selected_model_name=selected_model_name,
            is_active=False,
        )
        db.add(profile)
        await db.commit()
        await db.refresh(profile)

        logger.info(f"Created profile '{name}' for user {user_id} with provider {api_provider}")
        return profile

    @staticmethod
    async def update_profile(
        db: AsyncSession,
        profile_id: int,
        user_id: int,
        name: Optional[str] = None,
        api_provider: Optional[str] = None,
        api_key: Optional[str] = None,
        selected_model_name: Optional[str] = None,
    ) -> ConfigurationProfile:
        """Update a configuration profile."""
        result = await db.execute(
            select(ConfigurationProfile).where(
                ConfigurationProfile.id == profile_id, ConfigurationProfile.user_id == user_id
            )
        )
        profile = result.scalar_one_or_none()

        if not profile:
            raise ValueError(f"Profile {profile_id} not found or not owned by user")

        if name is not None:
            profile.name = name
        if api_provider is not None:
            profile.api_provider = api_provider
        if api_key is not None:
            profile.api_key = api_key
        if selected_model_name is not None:
            profile.selected_model_name = selected_model_name

        await db.commit()
        await db.refresh(profile)

        logger.info(f"Updated profile {profile_id}")
        return profile

    @staticmethod
    async def delete_profile(db: AsyncSession, profile_id: int, user_id: int) -> None:
        """Delete a configuration profile."""
        result = await db.execute(
            select(ConfigurationProfile).where(
                ConfigurationProfile.id == profile_id, ConfigurationProfile.user_id == user_id
            )
        )
        profile = result.scalar_one_or_none()

        if not profile:
            raise ValueError(f"Profile {profile_id} not found or not owned by user")

        await db.delete(profile)
        await db.commit()

        logger.info(f"Deleted profile {profile_id}")

    @staticmethod
    async def activate_profile(
        db: AsyncSession, profile_id: int, user_id: int
    ) -> ConfigurationProfile:
        """Activate a configuration profile (deactivates others)."""
        result = await db.execute(
            select(ConfigurationProfile).where(
                ConfigurationProfile.id == profile_id, ConfigurationProfile.user_id == user_id
            )
        )
        profile = result.scalar_one_or_none()

        if not profile:
            raise ValueError(f"Profile {profile_id} not found or not owned by user")

        # Deactivate all other profiles for this user
        # We do this manually to ensure consistency regardless of DB triggers
        from sqlalchemy import update

        await db.execute(
            update(ConfigurationProfile)
            .where(ConfigurationProfile.user_id == user_id)
            .values(is_active=False)
        )

        # Activate the selected profile
        profile.is_active = True
        await db.commit()
        await db.refresh(profile)

        logger.info(f"Activated profile {profile_id} for user {user_id}")
        return profile

    @staticmethod
    async def get_user_profiles(db: AsyncSession, user_id: int) -> list[ConfigurationProfile]:
        """Get all profiles for a user."""
        result = await db.execute(
            select(ConfigurationProfile)
            .where(ConfigurationProfile.user_id == user_id)
            .order_by(ConfigurationProfile.created_at.desc())
        )
        profiles = result.scalars().all()
        return list(profiles)

    @staticmethod
    async def get_active_profile(db: AsyncSession, user_id: int) -> Optional[ConfigurationProfile]:
        """Get user's currently active profile."""
        result = await db.execute(
            select(ConfigurationProfile)
            .where(ConfigurationProfile.user_id == user_id, ConfigurationProfile.is_active == True)
            .order_by(ConfigurationProfile.updated_at.desc())
        )
        profiles = result.scalars().all()

        # Defensive: Handle edge case of multiple active profiles
        if len(profiles) > 1:
            logger.warning(
                f"User {user_id} has {len(profiles)} active profiles. "
                f"This should not happen. Using most recently updated profile."
            )
            # Return the most recently updated one
            return profiles[0]
        elif len(profiles) == 1:
            return profiles[0]
        else:
            return None


# Global service instance
config_profile_service = ConfigProfileService()
