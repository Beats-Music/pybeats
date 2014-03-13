from pybeats.api import BeatsAPI
from _core import Object,PagingCollection

class Playlist(Object):
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

class PlaylistTracksCollection(PagingCollection):
    def __init__(self, relative_path, playlist_id, **kwargs):
        super(PlaylistTracksCollection, self).__init__(relative_path, **kwargs)
        self.playlist_id = playlist_id

    def _fetch_page(self, api, **kwargs):
        try:
            page_data = api._authed_get_collection(self.relative_path, **kwargs)
            self.total = page_data.get('info', {}).get('total')
            new_elements = page_data.get('data', [])
            self._process_data(new_elements)
        except Exception as err:
            print err
            # handle failure to get anything
            if self.total == -1:
                self.total = 0