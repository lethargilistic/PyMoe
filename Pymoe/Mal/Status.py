from enum import Enum
class SeriesStatus(Enum):
    Started = 1
    Finished = 2
    Planned = 3

class UserStatus(Enum):
    Watching = 1
    Completed = 2
    Onhold = 3
    Dropped = 4
    Planned = 6
