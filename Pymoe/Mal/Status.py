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
    Plantoenjoy = 6 #Yes, 6. MAL's API value.

class AnimeType(Enum):
    Unknown = 0
    TV = 1
    OVA = 2
    Movie = 3
    Special = 4
    ONA = 5
    Music = 6
    
class MangaType(Enum):
    Unknown = 0
    Manga = 1
    Novel = 2
    Oneshot = 3
    Doujinshi = 4
    Manhwa = 5
    Manhua = 6
