"""Initial schema

Revision ID: f15f0c2abf51
Revises:
Create Date: 2025-11-25 07:47:43.986390

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f15f0c2abf51"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), default=True, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)

    # Create conversations table
    op.create_table(
        "conversations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("is_visible", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_conversations_id"), "conversations", ["id"], unique=False)
    op.create_index(op.f("ix_conversations_user_id"), "conversations", ["user_id"], unique=False)

    # Create conversation_history table
    op.create_table(
        "conversation_history",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("conversation_id", sa.Integer(), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("is_visible_in_dashboard", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["conversation_id"], ["conversations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_conversation_history_conversation_id"),
        "conversation_history",
        ["conversation_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_conversation_history_id"), "conversation_history", ["id"], unique=False
    )

    # Create configuration_profiles table
    op.create_table(
        "configuration_profiles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("api_provider", sa.String(length=50), nullable=False),
        sa.Column("api_key", sa.Text(), nullable=False),
        sa.Column("selected_model_name", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_configuration_profiles_api_provider"),
        "configuration_profiles",
        ["api_provider"],
        unique=False,
    )
    op.create_index(
        op.f("ix_configuration_profiles_id"), "configuration_profiles", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_configuration_profiles_user_id"),
        "configuration_profiles",
        ["user_id"],
        unique=False,
    )

    # Create background_jobs table
    op.create_table(
        "background_jobs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("job_id", sa.String(length=255), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("conversation_id", sa.Integer(), nullable=True),
        sa.Column("task_name", sa.String(length=255), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "PENDING", "STARTED", "SUCCESS", "FAILURE", "RETRY", "REVOKED", name="jobstatus"
            ),
            nullable=False,
        ),
        sa.Column("input_message", sa.Text(), nullable=True),
        sa.Column("result", sa.Text(), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["conversation_id"],
            ["conversations.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_background_jobs_id"), "background_jobs", ["id"], unique=False)
    op.create_index(op.f("ix_background_jobs_job_id"), "background_jobs", ["job_id"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_background_jobs_job_id"), table_name="background_jobs")
    op.drop_index(op.f("ix_background_jobs_id"), table_name="background_jobs")
    op.drop_table("background_jobs")
    op.drop_index(op.f("ix_configuration_profiles_user_id"), table_name="configuration_profiles")
    op.drop_index(op.f("ix_configuration_profiles_id"), table_name="configuration_profiles")
    op.drop_index(
        op.f("ix_configuration_profiles_api_provider"), table_name="configuration_profiles"
    )
    op.drop_table("configuration_profiles")
    op.drop_index(op.f("ix_conversation_history_id"), table_name="conversation_history")
    op.drop_index(
        op.f("ix_conversation_history_conversation_id"), table_name="conversation_history"
    )
    op.drop_table("conversation_history")
    op.drop_index(op.f("ix_conversations_user_id"), table_name="conversations")
    op.drop_index(op.f("ix_conversations_id"), table_name="conversations")
    op.drop_table("conversations")
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS jobstatus")
