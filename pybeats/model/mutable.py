from pybeats.api import BeatsAPI
from _core import Object
from meta import User
from pybeats.utils import get_timezone

class Mutable(Object):

    def __init__(self, **data):
        super(Mutable, self).__init__(**data)

    # just for you

    def get_my_just_for_you(self, api, timezone=None, **kwargs):

        if timezone is None:
            timezone = get_timezone()

        payload = { 'time_zone' : timezone }
        payload.update(kwargs)
        coll = self._get_authed_collection(api, 'recs/just_for_you', **payload)
        # timestamp hack keeps the front of the collection pinned in time
        if coll.count > 0:
            coll.options['timestamp'] = coll.get_at(0).timestamp
        return coll

    # my library

    def get_my_library_artists(self, api, **kwargs):
        return self._get_authed_collection(api, 'mymusic/artists', **kwargs)

    def get_my_library_albums(self, api, **kwargs):
        return self._get_authed_collection(api, 'mymusic/albums', **kwargs)

    def get_my_library_tracks(self, api, **kwargs):
        return self._get_authed_collection(api, 'mymusic/tracks', **kwargs)

    # my playlists

    def get_my_playlists(self, api, **kwargs):
        return self._get_authed_collection(api, 'playlists', **kwargs)

    def get_my_playlist_subscriptions(self, api, **kwargs):
        return self._get_authed_collection(api, 'playlist_subscriptions', **kwargs)

class LoggedInUser(Mutable, User):

    def __init__(self, **data):
        super(LoggedInUser, self).__init__(**data)
