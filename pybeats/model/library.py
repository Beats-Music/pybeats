from meta import Album, Track, Artist

class MyMusicAlbum(Album):
    type = "mymusic_album"
    fields = ['mymusic_track_count', 'added_at', 'title', 'total_tracks', 'duration', 'release_date', 'release_format', 'rating', 'popularity', 'streamable', 'artist_display_name']
    refs = ['artists', 'label', 'tracks', 'user']

    def __init__(self, **data):
        super(MyMusicAlbum, self).__init__(**data)

    @property
    def relative_path(self):
        return "users/{0}/mymusic/{1}".format(self.user.identifier, self.identifier)

    def default_image_url(self, size):
        return "http://im.api.beatsmusic.com/api/albums/{0}/images/default?size={1}".format(self.identifier, size)


class MyMusicTrack(Track):
    type = "mymusic_track"
    fields = ['added_at', 'title', 'disc_number', 'parental_advisory', 'duration', 'track_position', 'popularity', 'streamable', 'artist_display_name']
    refs = ['artists', 'label', 'tracks', 'user']

    def __init__(self, **data):
        super(MyMusicTrack, self).__init__(**data)

    @property
    def relative_path(self):
        return "users/{0}/mymusic/{1}".format(self.user.identifier, self.identifier)

    def default_image_url(self, size):
        return "http://im.api.beatsmusic.com/api/tracks/{0}/images/default?size={1}".format(self.identifier, size)

class MyMusicArtist(Artist):
    type = "mymusic_artist"
    fields = ['name', 'popularity', 'total_singles', 'total_eps', 'total_lps', 'total_freeplays', 'total_compilations', 'streamable', 'total_albums', 'total_tracks']
    refs = ['artists', 'album', 'user']

    def __init__(self, **data):
        super(MyMusicArtist, self).__init__(**data)

    @property
    def relative_path(self):
        return "users/{0}/mymusic/{1}".format(self.user.identifier, self.identifier)

    def default_image_url(self, size):
        return "http://im.api.beatsmusic.com/api/artists/{0}/images/default?size={1}".format(self.identifier, size)
