from enum import IntEnum

from crud import CRUDStatus


Statuses = IntEnum(
    "Statuses",
    [
        (status.name.title(), status.id)
        for status in CRUDStatus.get_all_sync()
    ]
)