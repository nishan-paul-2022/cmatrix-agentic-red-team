#!/usr/bin/env python3
"""
Diagnostic script to test backend functionality
"""
import asyncio
import sys
from sqlalchemy import select

async def test_backend():
    """Test backend components"""
    print("=" * 60)
    print("CMatrix Backend Diagnostic Test")
    print("=" * 60)
    
    # Test 1: Database Connection
    print("\n[1/5] Testing database connection...")
    try:
        from app.core.database import get_db, init_db
        await init_db()
        print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
    
    # Test 2: Check for users
    print("\n[2/5] Checking for users...")
    try:
        from app.core.database import AsyncSessionLocal
        from app.models.user import User
        
        async with AsyncSessionLocal() as db:
            result = await db.execute(select(User))
            users = result.scalars().all()
            if users:
                print(f"✅ Found {len(users)} user(s)")
                for user in users:
                    print(f"   - User ID: {user.id}, Username: {user.username}")
            else:
                print("⚠️  No users found in database")
                print("   You may need to create a user account")
    except Exception as e:
        print(f"❌ Failed to query users: {e}")
        return False
    
    # Test 3: Check LLM Providers (ConfigurationProfile)
    print("\n[3/5] Checking LLM providers...")
    try:
        from app.core.database import AsyncSessionLocal
        from app.models.llm import ConfigurationProfile
        
        async with AsyncSessionLocal() as db:
            result = await db.execute(select(ConfigurationProfile))
            profiles = result.scalars().all()
            if profiles:
                print(f"✅ Found {len(profiles)} Configuration Profile(s)")
                for profile in profiles:
                    print(f"   - Profile: {profile.name}, Provider: {profile.api_provider}, Model: {profile.selected_model_name}")
                    print(f"     Active: {profile.is_active}, API Key Set: {'Yes' if profile.api_key else 'No'}")
            else:
                print("⚠️  No Configuration Profiles configured")
                print("   You need to configure an LLM provider in the settings")
                print("   This is likely causing the 500 errors!")
    except Exception as e:
        print(f"❌ Failed to query Configuration Profiles: {e}")
        return False
    
    # Test 4: Check Redis Connection
    print("\n[4/5] Testing Redis connection...")
    try:
        from app.worker import celery_app
        # Try to ping Redis through Celery
        result = celery_app.control.inspect().ping()
        if result:
            print(f"✅ Redis/Celery connection successful")
            print(f"   Active workers: {list(result.keys())}")
        else:
            print("⚠️  No Celery workers responding")
    except Exception as e:
        print(f"❌ Redis/Celery connection failed: {e}")
    
    # Test 5: Test Orchestrator
    print("\n[5/5] Testing orchestrator initialization...")
    try:
        from app.services.orchestrator import get_orchestrator_service
        orchestrator = get_orchestrator_service()
        print("✅ Orchestrator initialized successfully")
    except Exception as e:
        print(f"❌ Orchestrator initialization failed: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("Diagnostic Summary")
    print("=" * 60)
    print("\n⚠️  LIKELY ISSUE:")
    print("If you see 'No Configuration Profiles configured' above, that's your problem!")
    print("\nTO FIX:")
    print("Run the setup script:")
    print("python3 setup_llm.py")
    print("\n" + "=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        asyncio.run(test_backend())
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
