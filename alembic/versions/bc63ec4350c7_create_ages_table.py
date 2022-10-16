"""create ages table

Revision ID: bc63ec4350c7
Revises: b94deee9cf68
Create Date: 2022-08-23 19:51:10.443508

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc63ec4350c7'
down_revision = 'b94deee9cf68'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.add_column('vacancies', sa.Column('age_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'vacancies', 'ages', ['age_id'], ['id'], ondelete='NO ACTION')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'vacancies', type_='foreignkey')
    op.drop_column('vacancies', 'age_id')
    op.drop_table('ages')
    # ### end Alembic commands ###
