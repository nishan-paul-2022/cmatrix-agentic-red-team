"""Create system_settings table

Revision ID: add_system_settings
Revises:
Create Date: 2025-11-29

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "add_system_settings"
down_revision = "79d75099c35b"
depends_on = None


def upgrade():
    # Create system_settings table
    op.execute("""
        CREATE TABLE IF NOT EXISTS system_settings (
            key VARCHAR(255) PRIMARY KEY,
            value TEXT,
            description TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE
        );

        CREATE INDEX IF NOT EXISTS idx_system_settings_key ON system_settings(key);
    """)


def downgrade():
    op.drop_table("system_settings")
