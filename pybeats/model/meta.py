from pybeats.api import BeatsAPI
from _core import Object,AuthedObject

class Artist(Object):
    type = "artist"
    fields = ['name', 'popularity', 'total_singles', 'total_eps', 'total_lps', 'total_freeplays', 'total_compilations', 'streamable', 'total_albums', 'total_tracks']
    refs = []

    def __init__(self, **data):
        super(Artist, self).__init__(**data)

    @property
    def display_string(self):
        return self.name

    def get_albums(self, api, **kwargs):
        return self._get_collection(api,'albums', **kwargs)

    def get_tracks(self, api, **kwargs):
        return self._get_collection(api,'tracks', **kwargs)

    def get_playlists(self, api, **kwargs):
        return self._get_collection(api,'albums', **kwargs)

    def get_essential_albums(self, api, **kwargs):
        return self._get_collection(api,'essential_albums', **kwargs)

    def get_images(self, api, **kwargs):
        return self._get_collection(api,'images', **kwargs)

class Album(Object):
    type = "album"
    fields = ['title', 'total_tracks', 'duration', 'release_date','release_format', 'rating', 'popularity', 'streamable', 'artist_display_name']
    refs = ['artists', 'label', 'tracks']

    def __init__(self, **data):
        super(Album, self).__init__(**data)

    @property
    def display_string(self):
        return self.title

    def get_artists(self, api, **kwargs):
        return self._get_collection(api,'artists', **kwargs)

    def get_tracks(self, api, **kwargs):
        return self._get_collection(api,'tracks', **kwargs)

    def get_review(self, api, **kwargs):
        import editorial
        req_data = api.get_album_review(self.identifier, **kwargs)
        return editorial.Review(**req_data.get('data', {}))

    def get_companion_albums(self, api, **kwargs):
        return self._get_collection(api,'companion_albums', **kwargs)

class Track(Object):
    type = "track"
    fields = ['title', 'disc_number', 'parental_advisory', 'duration','track_position', 'popularity', 'streamable', 'artist_display_name']
    refs = ['artists', 'album']

    def __init__(self, **data):
        super(Track, self).__init__(**data)

    @property
    def display_string(self):
        return self.title

    def get_album(self, api, **kwargs):
        album_data = api.get_album_metadata(self.album.identifier, **kwargs).get('data', {})
        return Album(**album_data)

    def get_artists(self, api, **kwargs):
        return self._get_collection(api,'artists', **kwargs)

    def get_asset(self, api, **kwargs):
        import audio
        req_data = api.get_audio_asset(self.identifier, **kwargs)
        return audio.Asset(**req_data.get('data', {}))

class Genre(Object):
    type = "genre"
    fields = ['name', 'username', 'verified']
    refs = []

    def __init__(self, **data):
        super(Genre, self).__init__(**data)

    @property
    def display_string(self):
        return self.name

    def get_featured(self, api, **kwargs):
        return self._get_collection(api,'featured', **kwargs)

    def get_new_releases(self, api, **kwargs):
        return self._get_collection(api,'new_releases', **kwargs)

    def get_editors_picks(self, api, **kwargs):
        return self._get_collection(api,'editors_picks', **kwargs)

    def get_playlists(self, api, **kwargs):
        return self._get_authed_collection(api,'playlists', **kwargs)

    def get_bios(self, api, **kwargs):
        return self._get_collection(api,'bios', **kwargs)

    def get_images(self, api, **kwargs):
        return self._get_collection(api,'images', **kwargs)

class User(AuthedObject):
    type = "user"
    fields = ['username', 'full_name', 'verified']
    refs = []

    def __init__(self, **data):
        super(User, self).__init__(**data)

    @property
    def display_string(self):
        return self.full_name

    def get_playlists(self, api, **kwargs):
        return self._get_authed_collection(api, 'playlists', **kwargs)

    def get_images(self, api, **kwargs):
        return self._get_collection(api,'images', **kwargs)
