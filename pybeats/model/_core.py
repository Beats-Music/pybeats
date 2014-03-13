from pybeats.api import BeatsAPI

class Base(object):
    type = "unknown"
    fields = []
    refs = []

    def __init__(self, **data):
        self._update_from_data(data)

    def _update_from_data(self, data):
        self._update_fields_from_data(data)
        self._update_refs_from_refs(data.get('refs', []))

    def _update_fields_from_data(self, data):
        for field in self.fields:
            if field in data:
                setattr(self, 'identifier' if field == 'id' else field, data.get(field))

    def _update_refs_from_refs(self, refs):
        for ref in self.refs:
            if ref in refs:
                plural = ref[-1] == 's'
                if plural:
                    refarr = []
                    for refdata in refs[ref]:
                        refarr.append(Ref(**refdata))
                    setattr(self, ref, refarr)
                else:
                    setattr(self, ref, Ref(**refs[ref]))

    def serialize_to_dictionary(self, with_refs=True):
        obj = {}
        obj['type'] = self.type

        for field in self.fields:
            if hasattr(self, field):
                obj[field] = getattr(self, 'identifier' if field == 'id' else field)

        if not with_refs:
            return obj

        if len(self.refs) > 0:
            obj['refs'] = {}

        for ref in self.refs:
            if not hasattr(self, ref):
                continue
            plural = ref[-1] == 's'
            if plural:
                obj['refs'][ref] = []
                for r in getattr(self, ref):
                    obj['refs'][ref].append(r.serialize_to_dictionary())
            else:
                obj['refs'][ref] = getattr(self, ref).serialize_to_dictionary()

        return obj

    @staticmethod
    def class_for_type(data_type):
        import meta
        if data_type == 'album':
            return meta.Album
        elif data_type == 'artist':
            return meta.Artist
        elif data_type == 'track':
            return meta.Track
        return None

    @staticmethod
    def pluralize_type(data_type):
        if data_type == 'activity':
            return 'activities'
        else:
            return "{0}s".format(data_type)


class Ref(Base):
    type = "ref"
    fields = ['ref_type', 'display', 'id']

    def __init__(self, **data):
        super(Ref, self).__init__(**data)

    def create_full_object(self, api):
        cls = Base.class_for_type(self.ref_type)
        obj = cls(id=self.identifier)
        obj.fetch(api)
        return obj

    @property
    def relative_path(self):
        return "{0}/{1}".format(Base.pluralize_type(self.ref_type), self.identifier)

    def default_image_url(self, size):
        return "http://im.api.beatsmusic.com/api/{0}/{1}/images/default?size={2}".format(Base.pluralize_type(self.ref_type), self.identifier, size)


class Object(Base):

    def __init__(self, **data):
        super(Object, self).__init__(**data)

    def _update_from_data(self, data):
        self.identifier = data.get('id', '')
        super(Object, self)._update_from_data(data)

    def serialize_to_dictionary(self, with_refs=True):
        obj = super(Object, self).serialize_to_dictionary(with_refs)
        obj['id'] = self.identifier
        return obj

    @property
    def relative_path(self):
        return "{0}/{1}".format(Base.pluralize_type(self.type), self.identifier)

    def default_image_url(self, size):
        return "http://im.api.beatsmusic.com/api/{0}/images/default?size={1}".format(self.relative_path, size)

    @property
    def display_string(self):
        raise NotImplementedError(self.__class__.__name__ + '.display_string')

    def fetch(self, api, **kwargs):
        if self.identifier:
            data = api._get_resource_metadata(self.type, self.identifier, **kwargs).get('data')
            self._update_from_data(data)

    @classmethod
    def get(cls, api, **kwargs):
        coll = PagingCollection("{0}".format(Base.pluralize_type(cls.type)), **kwargs)
        coll.fetch_next(api)
        return coll

    def _get_collection(self, api, path, **kwargs):
        coll = PagingCollection("{0}/{1}".format(self.relative_path, path), **kwargs)
        coll.fetch_next(api)
        return coll

class Collection(object):

    def __init__(self, relative_path, **kwargs):
        self.relative_path = relative_path
        self.elements = []
        self.options = kwargs

    def __iter__(self):
        return self.elements.__iter__()

    def next(self):
        return self.elements.next()

    def get_at(self, index):
        return self.elements[index]

    def _process_datum(self, datum):
        cls = Base.class_for_type(datum.get('type', ''))
        self.elements.append(cls(**datum))

    def _process_data(self, data):
        for datum in data:
            self._process_datum(datum)

    def fetch(self, api, **kwargs):
        response_data = api._get_collection(self.relative_path, **payload)
        new_elements = response_data.get('data', [])
        self._process_data(new_elements)


class PagingCollection(Collection):

    def __init__(self, relative_path, **kwargs):
        super(PagingCollection, self).__init__(relative_path, **kwargs)
        self.total = -1
        self.page_size = 20

    def _fetch_page(self, api, **kwargs):
        page_data = api._get_collection(self.relative_path, **kwargs)
        try:
            self.total = page_data.get('info', {}).get('total')
            new_elements = page_data.get('data', [])
            self._process_data(new_elements)
        except Exception, err:
            # handle failure to get anything
            if self.total == -1:
                self.total = 0

    def fetch_next(self, api, **kwargs):
        if self.at_end:
            return

        payload = {
            'offset': self.count,
            'limit': self.page_size
        }
        payload.update(self.options)
        payload.update(kwargs)
        self._fetch_page(api, **payload)

    def fetch(self, api, **kwargs):
        while not self.at_end:
            self.fetch_next(api, **kwargs)

    # convenience name
    def fetch_rest(self, api, **kwargs):
        self.fetch(api, **kwargs)

    @property
    def count(self):
        return len(self.elements)

    @property
    def at_end(self):
        return self.total == self.count
