from enum import IntEnum

from crud import CRUDRole

Roles = IntEnum(
        "Roles",
        [
            (role.name.title(), role.id)
            for role in CRUDRole.get_all_sync()
        ]
    )
