from collections import namedtuple
from .Status import SeriesStatus, UserStatus

class _lazy_property(object):
    """
    lazy evaluation decorator
    derived from here: http://stackoverflow.com/a/6849299
    """
    def __init__(self,fget):
        self.fget = fget
        self.func_name = fget.__name__
    def __get__(self, obj, cls):
        if obj is None:
            return None
        value = self.fget(obj)
        setattr(obj, self.func_name, value)
        return value

class MediaList(list):
    def __init__(self, medialist):
        super().__init__(medialist)
        self.hashmap = dict()

        #TODO: Replace with n-bit vectors?
        #This is very expensive in space
        self.started_list = []
        self.finished_list = []
        self.planned_list = []

        self.u_watching_list = []
        self.u_completed_list = []
        self.u_onhold_list = []
        self.u_dropped_list = []
        self.u_planned_list = []

        for item in medialist:
            #Add the Media to a hashmap
            itemhash = hash(item)
            self.hashmap[hash(item)] = item

            #Add the hash to the category list it belongs to
            if item.status.series == SeriesStatus.Started:
                self.started_list.append(itemhash)
            elif item.status.series == SeriesStatus.Finished:
                self.finished_list.append(itemhash)
            elif item.status.series == SeriesStatus.Planned:
                self.planned_list.append(itemhash)
            else:
                raise ValueError("Series status is invalid: " + repr(item.status.series))

            if item.status.user == UserStatus.Watching:
                self.u_watching_list.append(itemhash)
            elif item.status.user == UserStatus.Completed:
                self.u_completed_list.append(itemhash)
            elif item.status.user == UserStatus.Onhold:
                self.u_onhold_list.append(itemhash)
            elif item.status.user == UserStatus.Dropped:
                self.u_dropped_list.append(itemhash)
            elif item.status.user == UserStatus.Planned:
                self.u_planned_list.append(itemhash)
            else:
                raise ValueError("User status is invalid: " + repr(item.status.user))

    #TODO: Decide if MediaList should be a fully implemented list subclass
    # Of if it should just be immutable, making these unnecesary
    """
    def __add__(...):
        #TODO: Also needs to add to hashmap, proper categories
        raise NotImplementedError
    def __delitem__(...):
        #TODO: Also needs to del from hashmap, proper categories
        raise NotImplementedError
    def __delslice__(...):
        raise NotImplementedError
    def __setslice__(...):
        raise NotImplementedError
    def __setslice__(...):
        raise NotImplementedError
    """

    def _processlist(self, alist):
        for i, itemhash in enumerate(alist):
            alist[i] = self.hashmap[itemhash]

        return alist

    # SeriesStatus
    @_lazy_property
    def started(self):
        for i, itemhash in enumerate(self.started_list):
            self.started_list[i] = self.hashmap[itemhash]

        return self.started_list

    @_lazy_property
    def finished(self):
        for i, itemhash in enumerate(self.finished_list):
            self.finished_list[i] = self.hashmap[itemhash]

        return self.finished_list

    @_lazy_property
    def planned(self):
        for i, itemhash in enumerate(self.planned_list):
            self.planned_list[i] = self.hashmap[itemhash]

        return self.planned_list

    # UserStatus
    @_lazy_property
    def watching(self):
        for i, itemhash in enumerate(self.u_watching_list):
            self.u_watching_list[i] = self.hashmap[itemhash]

        return self.u_watching_list

    @_lazy_property
    def completed(self):
        for i, itemhash in enumerate(self.u_completed_list):
            self.u_completed_list[i] = self.hashmap[itemhash]

        return self.u_completed_list

    @_lazy_property
    def onhold(self):
        for i, itemhash in enumerate(self.u_onhold_list):
            self.u_onhold_list[i] = self.hashmap[itemhash]

        return self.u_onhold_list

    @_lazy_property
    def dropped(self):
        for i, itemhash in enumerate(self.u_dropped_list):
            self.u_dropped_list[i] = self.hashmap[itemhash]

        return self.u_dropped_list
    
    #TODO: May change UserStatus.Planned -> UserStatus.Plantoenjoy
    @_lazy_property
    def planned_u(self):
        for i, itemhash in enumerate(self.u_planned_list):
            self.u_planned_list[i] = self.hashmap[itemhash]

        return self.u_planned_list

class NT_EPISODES:
    """
    Abstraction for Episode data. Total is the total number of episodes. Current is the user's current episode number.
    """
    def __init__(self, current, total):
        self.current = current
        self.total = total

    def __repr__(self):
        return 'NT_EPISODES(current={}, total={})'.format(repr(self.current), repr(self.total))


class NT_SCORES:
    """
    Abstraction for score data. Average is the score as per all ratings as returned by searches. user is the user's score for this item.
    """
    def __init__(self, average, user):
        self.average = average
        self.user = user

    def __repr__(self):
        return 'NT_SCORES(average={}, user={})'.format(repr(self.average), repr(self.user))


class NT_STATUS:
    """
    Abstraction for status data. Series is the anime or manga status. user is the user's status for this thing.
    """
    def __init__(self, series, user):
        self.series = series
        self.user = user

    def __repr__(self):
        return 'NT_STATUS(series={}, user={})'.format(repr(self.series), repr(self.user))


class NT_DATES:
    """
    Abstraction for dates. Series is the date data for the anime or manga as a whole. User is the user's start and finish dates.
    """
    def __init__(self, series, user):
        self.series = NT_DATE_OBJ(series)
        self.user = NT_DATE_OBJ(user)

    def __repr__(self):
        return 'NT_DATES(series={}, user={})'.format(repr(self.series), repr(self.user))


class NT_DATE_OBJ:
    """
    Abstraction for the individual start and end dates since both the users and series have start/end tuples.
    """
    def __init__(self, dates):
        self.start = dates[0]
        self.end = dates[1]

    def __repr__(self):
        return 'NT_DATE_OBJ(start={}, end={})'.format(repr(self.start), repr(self.end))


class NT_STORAGE:
    """
    Storage type/value abstraction.
    """
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return 'NT_STORAGE(type={}, value={})'.format(repr(self.type), repr(self.value))

class NT_REWATCHED:
    """
    Rewatched/Rereading times/value abstraction.
    """
    def __init__(self, times, value):
        self.times = times
        self.value = value

    def __repr__(self):
        return 'NT_REWATCHED(times={}, value={})'.format(repr(self.times), repr(self.value))


class NT_FLAGS:
    """
    Abstraction for flag data such as discussion enabling and rewatching/rereading enabling.
    """
    def __init__(self, discussion, rewatching=None, rereading=None):
        self.discussion = discussion
        self.rewatching = rewatching
        self.rereading = rereading

    def __repr__(self):
        return 'NT_FLAGS(discussion={}, rewatching={}, rereading={})'.format(repr(self.discussion),
                                                                             repr(self.rewatching),
                                                                             repr(self.rereading))


#: Abstraction for anime methods.
NT_ANIME = namedtuple('NT_ANIME', ['search', 'add', 'update', 'delete'])


#: Abstraction for manga methods.
NT_MANGA = namedtuple('NT_MANGA', ['search', 'add', 'update', 'delete'])


#: Abstraction for User Anime and Manga data.
NT_TYPEDATA = namedtuple('NT_TYPEDATA', ['list', 'stats'])


#: Abstraction for user anime and manga stats.
NT_STATS = namedtuple('NT_TYPESTATS', ['completed', 'onhold', 'dropped', 'planned', 'current', 'days'])

