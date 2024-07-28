from typing import Final


class Resources:
    class Map:
        CURRENT_ROOM_MARKER: Final = 'X'
        EXPLORED_ROOM_MARKER: Final = 'O'
        UNEXPLORED_ROOM_MARKER: Final = ' '
        ROOM_FORMAT: Final = '[{}]'
        EMPTY_SPACE: Final = '   '
