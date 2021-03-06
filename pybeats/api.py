from requests import request as requests_request

try:
    from urllib.parse import urlparse, parse_qs
except ImportError:
    from urlparse import urlparse, parse_qs

class BeatsAPI(object):

    base_url = 'https://partner.api.beatsmusic.com'
    base_path = '/v1/api'

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

        r = requests_request(method, self.base_url + path, **kwargs)

        try:
            return r.json()
        except:
            return None

    def _authed_request(self, method, path, **kwargs):

        if 'headers' not in kwargs:
            kwargs['headers'] = { 'Authorization' : 'Bearer {0}'.format(self.access_token) }
        else:
            kwargs['headers']['Authorization'] = 'Bearer {0}'.format(self.access_token)

        r = requests_request(method, self.base_url + path, **kwargs)

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

        data = self._request('post', '/oauth2/token', data=data, **kwargs)

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

        data = self._request('post', '/oauth2/token', data=data, **kwargs)

        if data is not None:
            self.refresh_token = data['result']['refresh_token']
            self.access_token = data['result']['access_token']

        return data

    def get_me(self):
        return self._authed_request('get', self.base_path + '/me')

    # basic metadata

    def _get_collection(self, path, prefix="/", **kwargs):
        return self._request('get', self.base_path + '{0}{1}'.format(prefix, path), params=kwargs)

    def _get_resource_metadata(self, resource_type, resource_id, **kwargs):
        return self._request('get', self.base_path + '/{0}s/{1}'.format(resource_type, resource_id), params=kwargs)

    def _get_resource_collection(self, resource_type, resource_id, collection_path, **kwargs):
        return self._get_collection(collection_path, prefix='/{0}s/{1}/'.format(resource_type, resource_id), **kwargs)

    def _authed_get_collection(self, path, prefix="/", **kwargs):
        return self._authed_request('get', self.base_path + '{0}{1}'.format(prefix, path), params=kwargs)

    def _authed_get_resource_metadata(self, resource_type, resource_id, **kwargs):
        return self._authed_request('get', self.base_path + '/{0}s/{1}'.format(resource_type, resource_id), params=kwargs)

    def _authed_get_resource_collection(self, resource_type, resource_id, collection_path, **kwargs):
        return self._authed_get_collection(collection_path, prefix='/{0}s/{1}/'.format(resource_type, resource_id), **kwargs)

    ## artists

    def get_artists(self, **kwargs):
        return self._get_collection('artists', **kwargs)

    def get_artist_metadata(self, artist_id, **kwargs):
        return self._get_resource_metadata('artist', artist_id, **kwargs)

    def get_artist_tracks(self, artist_id, **kwargs):
        return self._get_resource_collection('artist', artist_id, 'tracks', **kwargs)

    def get_artist_albums(self, artist_id, **kwargs):
        return self._get_resource_collection('artist', artist_id, 'albums', **kwargs)

    def get_artist_essential_albums(self, artist_id, **kwargs):
        return self._get_resource_collection('artist', artist_id, 'essential_albums', **kwargs)

    def get_artist_images(self, artist_id, **kwargs):
        return self._get_resource_collection('artist', artist_id, 'images', **kwargs)

    ## albums

    def get_albums(self, **kwargs):
        return self._get_collection('albums', **kwargs)

    def get_album_metadata(self, album_id, **kwargs):
        return self._get_resource_metadata('album', album_id, **kwargs)

    def get_album_artists(self, album_id, **kwargs):
        return self._get_resource_collection('album', album_id, 'artists', **kwargs)

    def get_album_tracks(self, album_id, **kwargs):
        return self._get_resource_collection('album', album_id, 'tracks', **kwargs)

    def get_album_review(self, album_id, **kwargs):
        return self._request('get', self.base_path + '/albums/{0}/review'.format(album_id), params=kwargs)

    def get_album_companion_albums(self, album_id, **kwargs):
        return self._get_resource_collection('album', album_id, 'companion_albums', **kwargs)

    ## tracks

    def get_tracks(self, **kwargs):
        return self._get_collection('tracks', **kwargs)

    def get_track_metadata(self, track_id, **kwargs):
        return self._get_resource_metadata('track', track_id, **kwargs)

    def get_track_artists(self, track_id, **kwargs):
        return self._get_resource_collection('track', album_id, 'artists', **kwargs)

    ## activities

    def get_activity(self, **kwargs):
        return self._get_collection('activities', **kwargs)

    def get_activity_metadata(self, activity_id, **kwargs):
        return self._get_resource_metadata('activitie', activity_id, **kwargs)

    def get_activity_editorial_playlists(self, activity_id, **kwargs):
        return self._get_resource_collection('activitie', activity_id, 'editorial_playlists', **kwargs)

    ## genres

    def get_genres(self, **kwargs):
        return self._get_collection('genres', **kwargs)

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
        return self._authed_get_resource_collection('genre', genre_id, 'playlists', **kwargs)

    def get_genre_images(self, genre_id, **kwargs):
        return self._get_resource_collection('genre', genre_id, 'images', **kwargs)

    ## users

    def get_user_metadata(self, user_id, **kwargs):
        return self._authed_get_resource_metadata('user', user_id, **kwargs)

    def get_user_playlists(self, user_id, **kwargs):
        return self._authed_get_resource_collection('user', user_id, 'playlists', **kwargs)

    def get_user_images(self, user_id, **kwargs):
        return self._authed_get_resource_collection('user', user_id, 'images', **kwargs)

    ## playlists

    def get_playlist_metadata(self, playlist_id, **kwargs):
        return self._authed_get_resource_metadata('playlist', playlist_id, **kwargs)

    def create_playlist(self, **kwargs):
        return self._authed_request('post', self.base_path + '/playlists', data=kwargs)

    def update_playlist(self, playlist_id, **kwargs):
        return self._authed_request('put', self.base_path + '/playlists/{0}'.format(playlist_id), data=kwargs)

    def delete_playlist(self, playlist_id):
        return self._authed_request('delete', self.base_path + '/playlists/{0}'.format(playlist_id))

    def get_playlist_tracks(self, playlist_id, **kwargs):
        return self._authed_get_resource_collection('playlist', playlist_id, 'tracks', **kwargs)

    def append_playlist_tracks(self, playlist_id, track_ids):
        payload = {
            'track_ids': track_ids
        }
        return self._authed_request('post', self.base_path + '/playlists/{0}/tracks'.format(playlist_id), data=payload)

    def update_playlist_tracks(self, playlist_id, track_ids):
        payload = {
            'track_ids': track_ids
        }
        return self._authed_request('put', self.base_path + '/playlists/{0}/tracks'.format(playlist_id), data=payload)

    def get_playlist_subscribers(self, playlist_id, **kwargs):
        return self._authed_get_resource_collection('playlist', playlist_id, 'subscribers', **kwargs)

    def get_playlists_for_user(self, user_id, **kwargs):
        return self._authed_get_resource_collection('user', user_id, 'playlists', **kwargs)

    def get_playlist_subscriptions_for_user(self, user_id, **kwargs):
        return self._authed_get_resource_collection('user', user_id, 'playlist_subscriptions', **kwargs)

    def subscribe_to_playlist(self, user_id, item_id):
        return self._authed_request('put', self.base_path + '/users/{0}/playlist_subscriptions/{1}'.format(user_id, item_id))

    def unsubscribe_from_playlist(self, user_id, item_id):
        return self._authed_request('delete', self.base_path + '/users/{0}/playlist_subscriptions/{1}'.format(user_id, item_id))

    def bulk_subscribe_to_playlists(self, user_id, item_ids):
        payload = {
            'ids': item_ids
        }
        return self._authed_request('post', self.base_path + '/users/{0}/playlist_subscriptions'.format(user_id), data=payload)

    def bulk_unsubscribe_from_playlists(self, user_id, item_ids):
        payload = {
            'ids': item_ids
        }
        return self._authed_request('delete', self.base_path + '/users/{0}/playlist_subscriptions'.format(user_id), params=payload)

    # recommendations

    def get_featured_content(self):
        return self._get_collection('discoveries/featured')

    def get_editors_picks(self):
        return self._get_collection('discoveries/editor_picks')

    def get_just_for_you(self, user_id, timezone, **kwargs):
        payload = { 'timezone' : timezone }
        payload.update(kwargs)
        return self._authed_get_resource_collection('user', user_id, 'recs/just_for_you', **payload)

    # search

    def get_search_results(self, query, search_type, **kwargs):
        payload = { 'q' : query, 'type' : search_type }
        payload.update(kwargs)
        return self._request('get', self.base_path + '/search', params=payload)

    def get_predictive_search_results(self, query, **kwargs):
        payload = { 'q' : query }
        payload.update(kwargs)
        return self._request('get', self.base_path + '/search/predictive', params=payload)

    # library

    def get_my_library_tracks(self, user_id):
        return self._authed_get_resource_collection('user', user_id, 'mymusic/tracks', **kwargs)

    def get_my_library_albums(self, user_id):
        return self._authed_get_resource_collection('user', user_id, 'mymusic/albums', **kwargs)

    def get_my_library_artists(self, user_id):
        return self._authed_get_resource_collection('user', user_id, 'mymusic/artists', **kwargs)

    def get_my_library_album_tracks(self, user_id, album_id, **kwargs):
        return self._authed_get_collection(collection_path, prefix='/users/{0}/mymusic/{1}/tracks'.format(user_id, album_id), **kwargs)

    def get_my_library_artist_tracks(self, user_id, artist_id, **kwargs):
        return self._authed_get_collection(collection_path, prefix='/users/{0}/mymusic/{1}/tracks'.format(user_id, artist_id), **kwargs)

    def get_my_library_artist_albums(self, user_id, artist_id, **kwargs):
        return self._authed_get_collection(collection_path, prefix='/users/{0}/mymusic/{1}/albums'.format(user_id, artist_id), **kwargs)

    def add_to_my_library(self, user_id, item_id):
        return self._authed_request('put', self.base_path + '/users/{0}/mymusic/{1}'.format(user_id, item_id))

    def remove_from_my_library(self, user_id, item_id):
        return self._authed_request('delete', self.base_path + '/users/{0}/mymusic/{1}'.format(user_id, item_id))

    def bulk_add_to_my_library(self, user_id, item_ids):
        payload = {
            'ids': item_ids
        }
        return self._authed_request('post', self.base_path + '/users/{0}/mymusic'.format(user_id), data=payload)

    def bulk_remove_from_my_library(self, user_id, item_ids):
        payload = {
            'ids': item_ids
        }
        return self._authed_request('delete', self.base_path + '/users/{0}/mymusic'.format(user_id), params=payload)

    # audio

    def get_audio_asset(self, track_id, **kwargs):
        return self._authed_request('get', self.base_path + '/tracks/{0}/audio'.format(track_id), params=kwargs)
