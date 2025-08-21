"""change id_etudiant to String

Revision ID: ed952a49db1c
Revises: 8ad93622a2f9
Create Date: 2025-08-21 13:27:23.573048

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'ed952a49db1c'
down_revision: Union[str, Sequence[str], None] = '8ad93622a2f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'etudiants',
        'id_etudiant',
        existing_type=sa.Integer(),
        type_=sa.String(length=50),
        existing_nullable=False,
        nullable=False
    )

def downgrade() -> None:
    op.alter_column(
        'etudiants',
        'id_etudiant',
        existing_type=sa.String(length=50),
        type_=sa.Integer(),
        existing_nullable=False,
        nullable=False
    )

