"""add_approval_logs_table

Revision ID: 79d75099c35b
Revises: f15f0c2abf51
Create Date: 2025-11-26 02:03:32.730305

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '79d75099c35b'
down_revision: Union[str, None] = 'f15f0c2abf51'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create approval_logs table for HITL approval audit trail."""
    op.create_table(
        'approval_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('thread_id', sa.String(length=255), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=True),
        sa.Column('tool_name', sa.String(length=255), nullable=False),
        sa.Column('tool_args', sa.JSON(), nullable=False),
        sa.Column('risk_level', sa.String(length=50), nullable=False),
        sa.Column('action', sa.String(length=50), nullable=False),  # 'approved' or 'rejected'
        sa.Column('reason', sa.Text(), nullable=True),
        sa.Column('modified_args', sa.JSON(), nullable=True),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for common queries
    op.create_index('idx_approval_logs_user_id', 'approval_logs', ['user_id'])
    op.create_index('idx_approval_logs_thread_id', 'approval_logs', ['thread_id'])
    op.create_index('idx_approval_logs_created_at', 'approval_logs', ['created_at'])
    op.create_index('idx_approval_logs_action', 'approval_logs', ['action'])
    op.create_index('idx_approval_logs_risk_level', 'approval_logs', ['risk_level'])

    # Add foreign key constraint to users table
    op.create_foreign_key(
        'fk_approval_logs_user_id',
        'approval_logs', 'users',
        ['user_id'], ['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    """Drop approval_logs table."""
    op.drop_constraint('fk_approval_logs_user_id', 'approval_logs', type_='foreignkey')
    op.drop_index('idx_approval_logs_risk_level', table_name='approval_logs')
    op.drop_index('idx_approval_logs_action', table_name='approval_logs')
    op.drop_index('idx_approval_logs_created_at', table_name='approval_logs')
    op.drop_index('idx_approval_logs_thread_id', table_name='approval_logs')
    op.drop_index('idx_approval_logs_user_id', table_name='approval_logs')
    op.drop_table('approval_logs')
