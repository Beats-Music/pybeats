from pybeats.api import BeatsAPI
from _core import AuthedObject,PagingAuthedCollection

class Playlist(AuthedObject):
    type = "playlist"
    fields = ['name', 'description', 'duration', 'created_at', 'updated_at', 'access', 'total_tracks', 'user_display_name', 'parental_advisory']
    refs = ['user', 'tracks']

    def __init__(self, **data):
        super(Playlist, self).__init__(**data)

    @property
    def display_string(self):
        return self.name

    # always gets them all, unlike most collections
    def get_tracks(self, api, **kwargs):
        coll = PlaylistTracksCollection("{0}/{1}".format(self.relative_path, 'tracks'), self.identifier, **kwargs)
        coll.fetch_rest(api)
        return coll

class PlaylistTracksCollection(PagingAuthedCollection):
    def __init__(self, relative_path, playlist_id, **kwargs):
        super(PlaylistTracksCollection, self).__init__(relative_path, **kwargs)
        self.playlist_id = playlist_id
