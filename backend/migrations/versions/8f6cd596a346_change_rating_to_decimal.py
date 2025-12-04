"""change_rating_to_decimal

Revision ID: 8f6cd596a346
Revises: 7ce106edf535
Create Date: 2025-12-04 11:39:18.265638

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f6cd596a346'
down_revision = '7ce106edf535'
branch_labels = None
depends_on = None


def upgrade():
    # Change rating column from Integer to Numeric(3,2) to support decimal ratings
    op.alter_column('movie', 'rating',
               existing_type=sa.INTEGER(),
               type_=sa.Numeric(3, 2),
               existing_nullable=True)


def downgrade():
    # Revert rating column back to Integer
    op.alter_column('movie', 'rating',
               existing_type=sa.Numeric(3, 2),
               type_=sa.INTEGER(),
               existing_nullable=True)
