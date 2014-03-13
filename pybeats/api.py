from requests import request as requests_request

try:
    from urllib.parse import urlparse, parse_qs
except ImportError:
    from urlparse import urlparse, parse_qs

class BeatsAPI(object):

    def __init__(self, client_id="", client_secret="", **kwargs):
        self.client_id = client_id
        self.client_secret = client_secret

    def __param_key_for_method(self, method):
        key = 'data'
        if method == 'GET' or method == 'DELETE':
            key = 'params'

        return key

    def __request(self, method, path, **kwargs):

        key = self.__param_key_for_method(method)

        if key not in kwargs:
            kwargs[key] = { 'client_id' : self.client_id }
        else:
            kwargs[key]['client_id'] = self.client_id

        r = requests_request(method, 'https://partner.api.beatsmusic.com/' + path, **kwargs)

        try:
            return r.json()
        except:
            return None

    def __authed_request(self, method, path, **kwargs):

        key = self.__param_key_for_method(method)

        if key not in kwargs:
            kwargs[key] = { 'access_token' : self.access_token }
        else:
            kwargs[key]['access_token'] = self.access_token

        r = requests_request(method, 'https://partner.api.beatsmusic.com/' + path, **kwargs)

        try:
            if r.status_code == 401 and 'stop' not in kwargs:
                self.refresh_token()
                return self.__authed_request(method, path, stop=True, **kwargs)
            else:
                return r.json()
        except:
            return None

    def __code(self, username, password, **kwargs):
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

    def __token(self, code, **kwargs):
        data = {
            'redirect_uri' : 'http://www.example.com',
            'client_secret' : self.client_secret,
            'code' : code
        }

        data = self.__request('post', 'oauth2/token', data=data, **kwargs)

        if data is not None:
            self.refresh_token = data['result']['refresh_token']
            self.access_token = data['result']['access_token']

        return data


    def login(self, username, password, **kwargs):
        code = self.__code(username, password)

        if code is None:
            return None

        return self.__token(code)

    def refresh_token(self, **kwargs):
        data = {
            'redirect_uri' : 'http://www.example.com',
            'client_secret' : self.client_secret,
            'grant_type' : 'refresh_token',
            'refresh_token' : self.refresh_token
        }

        data = self.__request('POST', 'oauth2/token', data=data, **kwargs)

        if data is not None:
            self.refresh_token = data['result']['refresh_token']
            self.access_token = data['result']['access_token']

        return data


