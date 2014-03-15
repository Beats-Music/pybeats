from pybeats.api import BeatsAPI
from _core import Object
from meta import User

class Mutable(Object):

    def __init__(self, **data):
        super(Mutable, self).__init__(**data)

    # my library

    def get_my_library_artists(self, api, **kwargs):
        return self._get_authed_collection(api, 'mymusic/artists')

    def get_my_library_albums(self, api, **kwargs):
        return self._get_authed_collection(api, 'mymusic/albums')

    def get_my_library_tracks(self, api, **kwargs):
        return self._get_authed_collection(api, 'mymusic/tracks')

    # my playlists

    def get_my_playlists(self, api, **kwargs):
        return self._get_authed_collection(api, 'playlists')

    def get_my_playlist_subscriptions(self, api, **kwargs):
        return self._get_authed_collection(api, 'playlist_subscriptions')

class LoggedInUser(Mutable, User):

    def __init__(self, **data):
        super(LoggedInUser, self).__init__(**data)