"""initial

Revision ID: 8e92f8ba245c
Revises: 
Create Date: 2022-08-22 16:30:50.493596

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e92f8ba245c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=24), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('citizen_ships',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('english',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('positions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['parent_id'], ['positions.id'], ondelete='NO ACTION'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.SmallInteger(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('statuses',
    sa.Column('id', sa.SmallInteger(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('work_experiences',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='NO ACTION'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('applicant_forms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_of_birth', sa.TIMESTAMP(), nullable=False),
    sa.Column('citizenship_id', sa.Integer(), nullable=False),
    sa.Column('is_married', sa.Boolean(), nullable=True),
    sa.Column('city_id', sa.Integer(), nullable=True),
    sa.Column('work_experience_id', sa.Integer(), nullable=False),
    sa.Column('phone_number', sa.CHAR(length=13), nullable=True),
    sa.Column('username', sa.Text(), nullable=True),
    sa.Column('instagram_url', sa.Text(), nullable=True),
    sa.Column('knowledge_of_english', sa.Integer(), nullable=False),
    sa.Column('position_id', sa.Integer(), nullable=False),
    sa.Column('is_published', sa.Boolean(), nullable=True),
    sa.Column('date_created', sa.TIMESTAMP(), nullable=True),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('surname', sa.Text(), nullable=False),
    sa.Column('patronymic', sa.Text(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['citizenship_id'], ['citizen_ships.id'], ondelete='NO ACTION'),
    sa.ForeignKeyConstraint(['city_id'], ['cities.id'], ondelete='NO ACTION'),
    sa.ForeignKeyConstraint(['knowledge_of_english'], ['english.id'], ondelete='NO ACTION'),
    sa.ForeignKeyConstraint(['position_id'], ['positions.id'], ondelete='NO ACTION'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='NO ACTION'),
    sa.ForeignKeyConstraint(['work_experience_id'], ['work_experiences.id'], ondelete='NO ACTION'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vacancies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('citizenship_id', sa.Integer(), nullable=False),
    sa.Column('city_id', sa.Integer(), nullable=True),
    sa.Column('work_experience_id', sa.Integer(), nullable=False),
    sa.Column('knowledge_of_english', sa.Boolean(), nullable=True),
    sa.Column('position_id', sa.Integer(), nullable=False),
    sa.Column('is_published', sa.Boolean(), nullable=True),
    sa.Column('date_created', sa.TIMESTAMP(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['citizenship_id'], ['citizen_ships.id'], ondelete='NO ACTION'),
    sa.ForeignKeyConstraint(['city_id'], ['cities.id'], ondelete='NO ACTION'),
    sa.ForeignKeyConstraint(['position_id'], ['positions.id'], ondelete='NO ACTION'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='NO ACTION'),
    sa.ForeignKeyConstraint(['work_experience_id'], ['work_experiences.id'], ondelete='NO ACTION'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('applicant_replies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('vacancy_id', sa.Integer(), nullable=False),
    sa.Column('status_id', sa.SmallInteger(), nullable=False),
    sa.ForeignKeyConstraint(['status_id'], ['statuses.id'], ondelete='NO ACTION'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['vacancy_id'], ['vacancies.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('employer_replies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('candidate_id', sa.BigInteger(), nullable=False),
    sa.Column('vacancy_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['candidate_id'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['vacancy_id'], ['vacancies.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('recent_jobs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('applicant_form_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['applicant_form_id'], ['applicant_forms.id'], ondelete='NO ACTION'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recent_jobs')
    op.drop_table('employer_replies')
    op.drop_table('applicant_replies')
    op.drop_table('vacancies')
    op.drop_table('applicant_forms')
    op.drop_table('users')
    op.drop_table('work_experiences')
    op.drop_table('statuses')
    op.drop_table('roles')
    op.drop_table('positions')
    op.drop_table('english')
    op.drop_table('citizen_ships')
    op.drop_table('cities')
    # ### end Alembic commands ###
