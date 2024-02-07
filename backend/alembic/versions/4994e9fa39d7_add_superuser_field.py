"""add superuser field

Revision ID: 4994e9fa39d7
Revises: 
Create Date: 2024-02-06 21:54:21.911597

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Boolean

# revision identifiers, used by Alembic.
revision: str = '4994e9fa39d7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # add is superuser column thats default False and is a boolean
    op.add_column("users",sa.Column("is_superuser", sa.Boolean,server_default='t',default=True))

def downgrade() -> None:
    op.add_column("users",sa.Column("is_superuser", sa.Boolean,server_default='t',default=True))
