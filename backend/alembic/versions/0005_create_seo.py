"""keywords, rank_trackings, site_audits, backlinks tabloları

Revision ID: 0005_create_seo
Revises: 0004_create_analytics
Create Date: 2026-05-29
"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0005_create_seo"
down_revision: str | None = "0004_create_analytics"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _ts():
    return (
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )


def upgrade() -> None:
    op.create_table(
        "keywords",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("term", sa.String(length=255), nullable=False),
        sa.Column("target_url", sa.String(length=512), nullable=True),
        sa.Column("search_volume", sa.Integer(), nullable=False),
        *_ts(),
        sa.ForeignKeyConstraint(["client_id"], ["clients.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_keywords_client_id"), "keywords", ["client_id"], unique=False)

    op.create_table(
        "rank_trackings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("keyword_id", sa.Integer(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        *_ts(),
        sa.ForeignKeyConstraint(["keyword_id"], ["keywords.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_rank_trackings_keyword_id"), "rank_trackings", ["keyword_id"], unique=False
    )

    op.create_table(
        "site_audits",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("issues", sa.JSON(), nullable=False),
        *_ts(),
        sa.ForeignKeyConstraint(["client_id"], ["clients.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_site_audits_client_id"), "site_audits", ["client_id"], unique=False)

    op.create_table(
        "backlinks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("source_url", sa.String(length=512), nullable=False),
        sa.Column("authority", sa.Integer(), nullable=False),
        sa.Column(
            "discovered_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        *_ts(),
        sa.ForeignKeyConstraint(["client_id"], ["clients.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_backlinks_client_id"), "backlinks", ["client_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_backlinks_client_id"), table_name="backlinks")
    op.drop_table("backlinks")
    op.drop_index(op.f("ix_site_audits_client_id"), table_name="site_audits")
    op.drop_table("site_audits")
    op.drop_index(op.f("ix_rank_trackings_keyword_id"), table_name="rank_trackings")
    op.drop_table("rank_trackings")
    op.drop_index(op.f("ix_keywords_client_id"), table_name="keywords")
    op.drop_table("keywords")
