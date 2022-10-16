from enum import IntEnum

from crud import CRUDEnglish

English = IntEnum(
        "English",
        [
            (english.name.title(), english.id)
            for english in CRUDEnglish.get_all_sync()
        ]
    )
