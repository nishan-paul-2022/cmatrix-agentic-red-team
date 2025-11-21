-- Fix Script: Resolve duplicate active configuration profiles
-- Description: Ensures only one active profile per user by keeping the most recently updated one
-- Date: 2025-11-21

-- Log affected profiles before fixing
DO $$
DECLARE
    affected_users RECORD;
    profile_record RECORD;
BEGIN
    RAISE NOTICE 'Starting duplicate active profile fix...';
    RAISE NOTICE '================================================';
    
    -- Show users with multiple active profiles
    FOR affected_users IN 
        SELECT user_id, COUNT(*) as active_count 
        FROM configuration_profiles 
        WHERE is_active = true 
        GROUP BY user_id 
        HAVING COUNT(*) > 1
    LOOP
        RAISE NOTICE 'User ID % has % active profiles:', affected_users.user_id, affected_users.active_count;
        
        -- Show all active profiles for this user
        FOR profile_record IN
            SELECT id, name, api_provider, updated_at
            FROM configuration_profiles
            WHERE user_id = affected_users.user_id AND is_active = true
            ORDER BY updated_at DESC
        LOOP
            RAISE NOTICE '  - Profile ID %: "%" (%), updated at %', 
                profile_record.id, 
                profile_record.name, 
                profile_record.api_provider,
                profile_record.updated_at;
        END LOOP;
    END LOOP;
    
    RAISE NOTICE '================================================';
END $$;

-- Fix: Deactivate all but the most recently updated profile per user
WITH ranked_profiles AS (
    SELECT 
        id,
        user_id,
        name,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY updated_at DESC) as rn
    FROM configuration_profiles
    WHERE is_active = true
)
UPDATE configuration_profiles cp
SET is_active = false
FROM ranked_profiles rp
WHERE cp.id = rp.id 
  AND rp.rn > 1;

-- Log the fix results
DO $$
DECLARE
    fixed_count INTEGER;
BEGIN
    GET DIAGNOSTICS fixed_count = ROW_COUNT;
    RAISE NOTICE 'Deactivated % duplicate active profiles', fixed_count;
    RAISE NOTICE '================================================';
    RAISE NOTICE 'Fix completed successfully!';
END $$;

-- Verify: Show current active profiles per user
SELECT 
    user_id,
    COUNT(*) as active_count,
    STRING_AGG(name || ' (' || api_provider || ')', ', ') as active_profiles
FROM configuration_profiles
WHERE is_active = true
GROUP BY user_id
ORDER BY user_id;
