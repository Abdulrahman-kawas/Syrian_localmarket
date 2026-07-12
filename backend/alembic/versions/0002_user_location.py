"""add users.last_location for proximity notifications

Idempotent: a database first created by 0001 already has the column (0001
baselines from the live ORM metadata via create_all), so this only adds it where
missing and creates the GiST index if absent.

Revision ID: 0002_user_location
Revises: 0001_initial
Create Date: 2026-07-13
"""

from __future__ import annotations

from alembic import op

revision = "0002_user_location"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS last_location"
        " geometry(Point, 4326)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_users_last_location "
        "ON users USING gist (last_location)"
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS idx_users_last_location")
    op.execute("ALTER TABLE users DROP COLUMN IF EXISTS last_location")
