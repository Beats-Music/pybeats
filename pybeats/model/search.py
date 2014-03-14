from pybeats.api import BeatsAPI
from _core import Object,Ref,Collection,PagingCollection

class SearchResult(Object):
    type = "search_result"
    fields = ['result_type', 'display', 'detail']

    def __init__(self, **data):
        super(SearchResult, self).__init__(**data)

    def _update_from_data(self, data):
        super(SearchResult, self)._update_from_data(data)
        self.related = Ref(**data.get('related', {}))

    def serialize_to_dictionary(self, with_refs=True):
        obj = super(SearchResult, self).serialize_to_dictionary(with_refs)
        obj['related'] = self.related.serialize_to_dictionary(with_refs)
        return obj

    @property
    def relative_path(self):
        raise NotImplementedError('SearchResult.relative_path')

    def default_image_url(self, size):
        return self.related.default_image_url(size)

    @property
    def display_string(self):
        return self.display

    @property
    def detail_string(self):
        return self.detail

    def fetch(self, api, **kwargs):
        raise NotImplementedError('SearchResult.fetch')

    @classmethod
    def get(cls, api, query=None, search_type=None, **kwargs):
        coll = PagingCollection("search")
        coll.options = {
            'type': search_type,
            'q': query
        }
        coll.fetch_next(api)
        return coll

    @classmethod
    def get_predictive(cls, api, query=None, **kwargs):
        coll = Collection("search/predictive")
        coll.options = {
            'q': query
        }
        coll.fetch(api)
        return coll