#!/usr/bin/env python3
"""
Script to setup LLM provider configuration
"""
import asyncio
import sys
from getpass import getpass
from sqlalchemy import select, update

async def setup_llm():
    """Setup LLM provider configuration"""
    print("=" * 60)
    print("CMatrix LLM Configuration Setup")
    print("=" * 60)
    
    try:
        from app.core.database import AsyncSessionLocal
        from app.models.llm import ConfigurationProfile, APIProvider
        from app.models.user import User
        
        async with AsyncSessionLocal() as db:
            # Get user
            result = await db.execute(select(User))
            users = result.scalars().all()
            
            if not users:
                print("❌ No users found. Please create a user account first.")
                return
            
            user = users[0]
            print(f"Configuring for user: {user.username} (ID: {user.id})")
            
            # Select Provider
            print("\nAvailable Providers:")
            providers = [p.value for p in APIProvider]
            for i, p in enumerate(providers):
                print(f"{i+1}. {p}")
            
            while True:
                try:
                    choice = int(input("\nSelect provider (number): "))
                    if 1 <= choice <= len(providers):
                        provider = providers[choice-1]
                        break
                    print("Invalid selection.")
                except ValueError:
                    print("Please enter a number.")
            
            # Get API Key
            api_key = getpass(f"\nEnter API Key for {provider}: ")
            if not api_key:
                print("API Key cannot be empty.")
                return
            
            # Get Model Name (Optional)
            model_name = input("Enter Model Name (optional, press Enter for default): ").strip()
            
            # Create or Update Profile
            # Check if profile exists for this provider
            result = await db.execute(
                select(ConfigurationProfile).where(
                    ConfigurationProfile.user_id == user.id,
                    ConfigurationProfile.api_provider == provider
                )
            )
            existing_profile = result.scalar_one_or_none()
            
            if existing_profile:
                print(f"\nUpdating existing profile for {provider}...")
                existing_profile.api_key = api_key
                if model_name:
                    existing_profile.selected_model_name = model_name
                existing_profile.is_active = True
                
                # Deactivate others
                await db.execute(
                    update(ConfigurationProfile)
                    .where(ConfigurationProfile.id != existing_profile.id)
                    .values(is_active=False)
                )
            else:
                print(f"\nCreating new profile for {provider}...")
                # Deactivate all others first
                await db.execute(
                    update(ConfigurationProfile)
                    .where(ConfigurationProfile.user_id == user.id)
                    .values(is_active=False)
                )
                
                new_profile = ConfigurationProfile(
                    user_id=user.id,
                    name=f"{provider} Default",
                    api_provider=provider,
                    api_key=api_key,
                    selected_model_name=model_name,
                    is_active=True
                )
                db.add(new_profile)
            
            await db.commit()
            print("\n✅ Configuration saved and activated successfully!")
            print("You can now use the chat feature.")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        asyncio.run(setup_llm())
    except KeyboardInterrupt:
        print("\nSetup cancelled.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
