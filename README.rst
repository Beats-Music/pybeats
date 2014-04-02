Beats Music Developer Platform SDK (Python)
===========================================

Overview
--------

The SDK has effectively two interfaces with the developer platform: the
API object and the suite of models. The API object is just a small
wrapper around network calls that for small one-off interactions with
the service. Models are preferrable for larger, more complex options,
and are a bit more user-friendly.

Getting Started
---------------

Before doing anything, head over to https://developer.beatsmusic.com and
apply for a partner key if you don’t one. You’ll want to know both your
client id and your client secret (though some calls only need the client
id).

After that, you can install this package with ``pip``.

::

    pip install git+https://github.com/Beats-Music/pybeats.git

Models
------

The two “base” classes of the model framework are ``Base`` (aptly named)
and ``Collection``. Single resources all extend ``Base`` with resource
collections all extend ``Collection``.

``Base`` provides serialization to and from JSON, exposing the JSON
object properties as properties of the class instance. If a resource has
an id (tracks, playlists, users, etc.) they extend the ``Object`` class
(which extends ``Base``). All of these classes convert the json ``id``
property to the ``identifier`` property on the class instance.

The primary feature of a ``Collection`` is that it will convert all
incoming data to their respective models for you. If a collection
supports paging, the ``PagingCollection`` will let you access data one
page at a time. Most resource collections are paging collections.

::

    from pybeats.api import BeatsAPI
    from pybeats.model import Collection,SearchResult,LoggedInUser

    CLIENT_ID = "your-id-here"
    CLIENT_SECRET = "your-secret-here"

    USERNAME = "your-beats-username"
    PASSWORD = "your-beats-password"

    # set up your api instance
    api = BeatsAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

    # some "open calls" you can do now

    # searching
    search_results = SearchResult.get(api, query='99 Problems', search_type='track')
    for result in search_results:
        print "{0} - {1} (id: {2})".format(result.display, result.detail, result.identifier)


    # featured content
    featured = Collection("discoveries/featured")
    for feature in featured:
        print feature.content.display_string

    # calls that require some auth

    # login as your user
    api.login(USERNAME, PASSWORD)

    # getting your account information
    my_data = api.get_me()
    user_id = my_data['result']['user_context']

    my_user = LoggedInUser(id=user_id)
    my_user.fetch(api)

    print my_user.username

    my_playlists = my_user.get_playlists(api)
    my_playlists.fetch_next(api)
    for playlist in my_playlists:
        print "{0} by {1}".format(playlist.display_string, playlist.user.display)

API Interface
-------------

All of the models use the API interface under the covers. However, for
some one-off its might be user to use the API interface directly. The
following examples are basically a translation of the ones presented
above.

::

    from pybeats.api import BeatsAPI

    CLIENT_ID = "your-id-here"
    CLIENT_SECRET = "your-secret-here"

    USERNAME = "your-beats-username"
    PASSWORD = "your-beats-password"

    # set up your api instance
    api = BeatsAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

    # some "open calls" you can do now

    # searching
    search_results = api.get_search_results('99 Problems', 'track')
    for result in search_results['data']:
        print "{0} - {1} (id: {2})".format(result['display'], result['detail'], result['id'])


    # featured content
    featured = api.get_featured_content()
    for feature in featured['data']:
        print feature

    # calls that require some auth

    # login as your user
    api.login(USERNAME, PASSWORD)

    # getting your account information
    my_data = api.get_me()
    user_id = my_data['result']['user_context']

    user_data = api.get_user_metadata(user_id)
    print user_data['data']['username']

    my_playlists = api.get_user_playlists(user_id)
    for playlist in my_playlists['data']:
        print "{0} by {1}".format(playlist['name], playlist['refs']['user']['display'])

