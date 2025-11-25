# Legacy SQL Migrations

These SQL migration files are **no longer used** in the project.

## Migration System

The project now uses **Alembic** for database migrations (Python-based, version-controlled).

## Files in This Directory

- `001_add_conversations.sql` - Initial conversations table setup
- `002_add_llm_models.sql` - LLM models configuration
- `003_configuration_profiles.sql` - Configuration profiles
- `fix_duplicate_active_profiles.sql` - Data fix for duplicate profiles

## Why These Are Here

These files are kept for **historical reference only**. They show the evolution of the database schema but are not executed.

## Current Migration System

Use Alembic for all migrations:

```bash
# Run migrations
cd backend
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "Description"
```

See `MIGRATION_GUIDE.md` in the project root for complete documentation.

---

**Status:** ⚠️ **ARCHIVED** - Do not use these files
**Replaced by:** Alembic migrations in `migrations/versions/`
