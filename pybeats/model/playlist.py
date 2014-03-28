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

    def append_tracks(self, api, tracks):
        track_ids = [track.identifier for track in tracks]
        api.append_playlist_tracks(self.identifier, track_ids)

    def save(self, api, **kwargs):
        self_obj = self.serialize_to_dictionary(with_refs=False)

        if self.identifier is not '':
            data = api.update_playlist(self.identifier, **self_obj)
        else:
            data = api.create_playlist(**self_obj)
        self._update_from_data(data.get('data', {}))

    def destroy(self, api):
        api.delete_playlist(self.identifier)

class PlaylistTracksCollection(PagingAuthedCollection):

    def __init__(self, relative_path, playlist_id, **kwargs):
        super(PlaylistTracksCollection, self).__init__(relative_path, **kwargs)
        self.playlist_id = playlist_id

    def set_tracks(self, tracks):
        # empty
        self.elements[:] = []
        self.elements.extend(tracks)

    def add_track(self, track):
        self.elements.append(track)

    def save(self, api, **kwargs):
        track_ids = [track.identifier for track in self.elements]
        data = api.update_playlist_tracks(self.playlist_id, track_ids)
