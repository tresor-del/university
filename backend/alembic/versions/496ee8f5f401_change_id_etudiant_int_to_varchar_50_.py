"""change id_etudiant INT to VARCHAR(50) NOT NULL

Revision ID: 496ee8f5f401
Revises: ed952a49db1c
Create Date: 2025-08-21 13:39:04.362495

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '496ee8f5f401'
down_revision: Union[str, Sequence[str], None] = 'ed952a49db1c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
