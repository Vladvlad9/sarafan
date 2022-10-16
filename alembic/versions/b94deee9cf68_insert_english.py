"""insert english

Revision ID: b94deee9cf68
Revises: e8e3d57b7e99
Create Date: 2022-08-22 16:34:16.411013

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import English, create_sync_session


# revision identifiers, used by Alembic.
revision = 'b94deee9cf68'
down_revision = 'e8e3d57b7e99'
branch_labels = None
depends_on = None

values = [
    'А1 (Beginner)',
    'А2 (Elementary)',
    'В1 (Intermediate)',
    'В2 (Upper Intermediate)',
    'С1 (Advanced)',
    'С2 (Proficiency)'
]


@create_sync_session
def upgrade(session: Session = None) -> None:
    for value in values:
        value = English(name=value)
        session.add(value)
        try:
            session.commit()
        except IntegrityError:
            pass


@create_sync_session
def downgrade(session: Session = None) -> None:
    for value in values:
        session.execute(
            sa.delete(English)
            .where(English.name == value)
        )
        session.commit()
