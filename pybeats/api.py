from requests import request as requests_request

try:
    from urllib.parse import urlparse, parse_qs
except ImportError:
    from urlparse import urlparse, parse_qs

class BeatsAPI(object):

    def __init__(self, client_id="", client_secret="", **kwargs):
        self.client_id = client_id
        self.client_secret = client_secret

    def __request(self, method, url, **kwargs):
        r = requests_request(method, url, **kwargs)
        try:
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
        r = requests_request('POST', 'https://partner.api.beatsmusic.com/api/o/oauth2/approval', data=data, headers=headers, allow_redirects=False, **kwargs)

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
            'client_id' : self.client_id,
            'client_secret' : self.client_secret,
            'code' : code
        }

        return self.__request('POST', 'https://partner.api.beatsmusic.com/oauth2/token', data=data, **kwargs)


    def login(self, username, password, **kwargs):
        code = self.__code(username, password)

        if code is None:
            return None

        return self.__token(code)

    def refresh_token(self, refresh_token, **kwargs):
        data = {
            'redirect_uri' : 'http://www.example.com',
            'client_id' : self.client_id,
            'client_secret' : self.client_secret,
            'grant_type' : 'refresh_token',
            'refresh_token' : refresh_token
        }
        return self.__request('POST', 'https://partner.api.beatsmusic.com/oauth2/token', data=data, **kwargs)



