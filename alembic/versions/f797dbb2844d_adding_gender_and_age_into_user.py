"""adding gender and age into User

Revision ID: f797dbb2844d
Revises: 6f5e6b27045c
Create Date: 2024-11-28 09:55:32.499533

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f797dbb2844d'
down_revision: Union[str, None] = '6f5e6b27045c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('clients', sa.Column('Gender', sa.String(), nullable=True))
    op.add_column('clients', sa.Column('age', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_clients_Gender'), 'clients', ['Gender'], unique=False)
    op.create_index(op.f('ix_clients_age'), 'clients', ['age'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_clients_age'), table_name='clients')
    op.drop_index(op.f('ix_clients_Gender'), table_name='clients')
    op.drop_column('clients', 'age')
    op.drop_column('clients', 'Gender')
    # ### end Alembic commands ###