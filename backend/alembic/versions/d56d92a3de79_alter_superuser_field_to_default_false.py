"""alter superuser field to default false

Revision ID: d56d92a3de79
Revises: 4994e9fa39d7
Create Date: 2024-02-07 07:44:18.448985

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd56d92a3de79'
down_revision: Union[str, None] = '4994e9fa39d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("users",sa.Column("is_superuser", sa.Boolean,server_default='f',default=False))


def downgrade() -> None:
    op.alter_column("users",sa.Column("is_superuser", sa.Boolean,server_default='f',default=False))
