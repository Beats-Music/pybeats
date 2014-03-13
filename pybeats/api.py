from requests import request as requests_request

try:
    from urllib.parse import urlparse, parse_qs
except ImportError:
    from urlparse import urlparse, parse_qs

class BeatsAPI(object):

    def __init__(self, client_id="", client_secret="", **kwargs):
        self.client_id = client_id
        self.client_secret = client_secret

    def _param_key_for_method(self, method):
        key = 'data'
        if method == 'GET' or method == 'DELETE':
            key = 'params'

        return key

    def _request(self, method, path, **kwargs):

        key = self._param_key_for_method(method)

        if key not in kwargs:
            kwargs[key] = { 'client_id' : self.client_id }
        else:
            kwargs[key]['client_id'] = self.client_id

        r = requests_request(method, 'https://partner.api.beatsmusic.com/' + path, **kwargs)

        try:
            return r.json()
        except:
            return None

    def _authed_request(self, method, path, **kwargs):

        key = self._param_key_for_method(method)

        if key not in kwargs:
            kwargs[key] = { 'access_token' : self.access_token }
        else:
            kwargs[key]['access_token'] = self.access_token

        r = requests_request(method, 'https://partner.api.beatsmusic.com/' + path, **kwargs)

        try:
            if r.status_code == 401 and 'stop' not in kwargs:
                self.refresh_token()
                return self._authed_request(method, path, stop=True, **kwargs)
            else:
                return r.json()
        except:
            return None

    def _code(self, username, password, **kwargs):
        data = {
            'login' : username,
            'password' : password,
            'redirect_uri' : 'http://www.example.com',
            'client_id' : self.client_id,
            'response_type' : 'code',
            'state' : '',
            'scope' : None,
            'user_id' : None
        }
        headers = {
            'Referer' : 'https://partner.api.beatsmusic.com/oauth2/authorize'
        }
        r = requests_request('post', 'https://partner.api.beatsmusic.com/api/o/oauth2/approval', data=data, headers=headers, allow_redirects=False, **kwargs)

        try :
            location = r.headers['location']
            parsed = urlparse(location)
            qs = parse_qs(parsed.query, keep_blank_values=True)
            code = qs['code'][0]
            return code
        except:
            return None

    def _token(self, code, **kwargs):
        data = {
            'redirect_uri' : 'http://www.example.com',
            'client_secret' : self.client_secret,
            'code' : code
        }

        data = self._request('post', 'oauth2/token', data=data, **kwargs)

        if data is not None:
            self.refresh_token = data['result']['refresh_token']
            self.access_token = data['result']['access_token']

        return data


    def login(self, username, password, **kwargs):
        code = self._code(username, password)

        if code is None:
            return None

        return self._token(code)

    def refresh_token(self, **kwargs):
        data = {
            'redirect_uri' : 'http://www.example.com',
            'client_secret' : self.client_secret,
            'grant_type' : 'refresh_token',
            'refresh_token' : self.refresh_token
        }

        data = self._request('POST', 'oauth2/token', data=data, **kwargs)

        if data is not None:
            self.refresh_token = data['result']['refresh_token']
            self.access_token = data['result']['access_token']

        return data

    # basic metadata

    def _get_collection(self, path, prefix="", **kwargs):
        return self._request('get', '{0}{1}'.format(prefix, path), params=kwargs)

    def _get_resource_metadata(self, resource_type, resource_id, **kwargs):
        return self._request('get', 'v1/api/{0}s/{1}'.format(resource_type, resource_id), params=kwargs)

    def _get_resource_collection(self, resource_type, resource_id, collection_path, **kwargs):
        return self._get_collection(collection_path, prefix='v1/api/{0}s/{1}'.format(resource_type, resource_id), **kwargs)


    ## artists

    def get_artists(self, **kwargs):
        return self._get_collection('v1/api/artists', **kwargs)

    def get_artist_metadata(self, artist_id, **kwargs):
        return self._get_resource_metadata('artist', artist_id, **kwargs)

    def get_artist_tracks(self, artist_id, **kwargs):
        return self._get_resource_collection('artist', artist_id, 'tracks', **kwargs)

    def get_artist_albums(self, artist_id, **kwargs):
        return self._get_resource_collection('artist', artist_id, 'albums', **kwargs)

    def get_artist_essential_albums(self, artist_id, **kwargs):
        return self._get_resource_collection('artist', artist_id, 'essential_albums', **kwargs)

    ## albums

    def get_albums(self, **kwargs):
        return self._get_collection('v1/api/albums', **kwargs)

    def get_album_metadata(self, album_id, **kwargs):
        return self._get_resource_metadata('album', album_id, **kwargs)

    def get_album_artists(self, album_id, **kwargs):
        return self._get_resource_collection('album', album_id, 'artists', **kwargs)

    def get_album_tracks(self, album_id, **kwargs):
        return self._get_resource_collection('album', album_id, 'tracks', **kwargs)

    def get_album_reviews(self, album_id, **kwargs):
        return self._get_resource_collection('album', album_id, 'reviews', **kwargs)

    def get_album_companion_albums(self, album_id, **kwargs):
        return self._get_resource_collection('album', album_id, 'companion_albums', **kwargs)

    ## tracks

    def get_tracks(self, **kwargs):
        return self._get_collection('v1/api/tracks', **kwargs)

    def get_track_metadata(self, track_id, **kwargs):
        return self._get_resource_metadata('track', track_id, **kwargs)

    def get_track_artists(self, track_id, **kwargs):
        return self._get_resource_collection('track', album_id, 'artists', **kwargs)

    ## activities

    def get_activity(self, **kwargs):
        return self._get_collection('v1/api/activities', **kwargs)

    def get_activity_metadata(self, activity_id, **kwargs):
        return self._get_resource_metadata('activitie', activity_id, **kwargs)

    def get_activity_editorial_playlists(self, activity_id, **kwargs):
        return self._get_resource_collection('activitie', activity_id, 'editorial_playlists', **kwargs)

    ## genres

    def get_genres(self, **kwargs):
        return self._get_collection('v1/api/genres', **kwargs)

    def get_genre_metadata(self, genre_id, **kwargs):
        return self._get_resource_metadata('genre', genre_id, **kwargs)

    def get_genre_editors_picks(self, genre_id, **kwargs):
        return self._get_resource_collection('genre', genre_id, 'editors_picks', **kwargs)

    def get_genre_featured(self, genre_id, **kwargs):
        return self._get_resource_collection('genre', genre_id, 'featured', **kwargs)

    def get_genre_new_releases(self, genre_id, **kwargs):
        return self._get_resource_collection('genre', genre_id, 'new_releases', **kwargs)

    def get_genre_bios(self, genre_id, **kwargs):
        return self._get_resource_collection('genre', genre_id, 'bios', **kwargs)

    def get_genre_playlists(self, genre_id, **kwargs):
        return self._get_resource_collection('genre', genre_id, 'playlists', **kwargs)