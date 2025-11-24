"""Add background_jobs table

Revision ID: add_background_jobs
Revises: 
Create Date: 2025-11-25

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_background_jobs'
down_revision = None  # Update this with your latest migration ID
branch_labels = None
depends_on = None


def upgrade():
    """Create background_jobs table."""
    op.create_table(
        'background_jobs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('job_id', sa.String(length=255), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=True),
        sa.Column('task_name', sa.String(length=255), nullable=False),
        sa.Column('status', sa.Enum('pending', 'started', 'success', 'failure', 'retry', 'revoked', name='jobstatus'), nullable=False),
        sa.Column('input_message', sa.Text(), nullable=True),
        sa.Column('result', sa.Text(), nullable=True),
        sa.Column('error', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_background_jobs_id'), 'background_jobs', ['id'], unique=False)
    op.create_index(op.f('ix_background_jobs_job_id'), 'background_jobs', ['job_id'], unique=True)


def downgrade():
    """Drop background_jobs table."""
    op.drop_index(op.f('ix_background_jobs_job_id'), table_name='background_jobs')
    op.drop_index(op.f('ix_background_jobs_id'), table_name='background_jobs')
    op.drop_table('background_jobs')
    op.execute('DROP TYPE jobstatus')
