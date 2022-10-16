"""insert roles

Revision ID: 906256cfcd17
Revises: c6a2307f520f
Create Date: 2022-08-09 14:09:54.286991

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import Role, create_sync_session


# revision identifiers, used by Alembic.
revision = '906256cfcd17'
down_revision = '8e92f8ba245c'
branch_labels = None
depends_on = None


roles = ['admin', 'support', 'employer', 'applicant']


@create_sync_session
def upgrade(session: Session = None) -> None:
    for role in roles:
        role = Role(name=role)
        session.add(role)
        try:
            session.commit()
        except IntegrityError:
            pass


@create_sync_session
def downgrade(session: Session = None) -> None:
    for role in roles:
        session.execute(
            sa.delete(Role)
            .where(Role.name == role)
        )
        session.commit()
