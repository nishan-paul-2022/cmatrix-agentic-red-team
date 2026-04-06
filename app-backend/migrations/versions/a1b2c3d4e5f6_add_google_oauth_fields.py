"""Add Google OAuth fields to users table

Revision ID: a1b2c3d4e5f6
Revises: 79d75099c35b
Create Date: 2026-04-06 16:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = "add_system_settings"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Make hashed_password nullable (OAuth users won't have a password)
    op.alter_column(
        "users",
        "hashed_password",
        existing_type=sa.String(length=255),
        nullable=True,
    )

    # Add email column (unique, indexable)
    op.add_column(
        "users",
        sa.Column("email", sa.String(length=255), nullable=True),
    )
    op.create_unique_constraint("uq_users_email", "users", ["email"])
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    # Add google_id (the unique Google Subject ID)
    op.add_column(
        "users",
        sa.Column("google_id", sa.String(length=255), nullable=True),
    )
    op.create_unique_constraint("uq_users_google_id", "users", ["google_id"])
    op.create_index("ix_users_google_id", "users", ["google_id"], unique=True)

    # Add avatar_url for Google profile picture
    op.add_column(
        "users",
        sa.Column("avatar_url", sa.String(length=512), nullable=True),
    )

    # Add auth_provider to distinguish local vs oauth users
    op.add_column(
        "users",
        sa.Column(
            "auth_provider",
            sa.String(length=50),
            nullable=False,
            server_default="local",
        ),
    )


def downgrade() -> None:
    op.drop_column("users", "auth_provider")
    op.drop_column("users", "avatar_url")
    op.drop_index("ix_users_google_id", table_name="users")
    op.drop_constraint("uq_users_google_id", "users", type_="unique")
    op.drop_column("users", "google_id")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_constraint("uq_users_email", "users", type_="unique")
    op.drop_column("users", "email")
    op.alter_column(
        "users",
        "hashed_password",
        existing_type=sa.String(length=255),
        nullable=False,
    )
