"""insert statuses

Revision ID: e8e3d57b7e99
Revises: 906256cfcd17
Create Date: 2022-08-09 14:13:01.103806

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models import Status, create_sync_session


# revision identifiers, used by Alembic.
revision = 'e8e3d57b7e99'
down_revision = '906256cfcd17'
branch_labels = None
depends_on = None

statuses = ['sent', 'rejected', 'review', 'approved']


@create_sync_session
def upgrade(session: Session = None) -> None:
    for status in statuses:
        status = Status(name=status)
        session.add(status)
        try:
            session.commit()
        except IntegrityError:
            pass


@create_sync_session
def downgrade(session: Session = None) -> None:
    for status in statuses:
        session.execute(
            sa.delete(Status)
            .where(Status.name == status)
        )
        session.commit()
