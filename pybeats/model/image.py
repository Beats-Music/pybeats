from _core import Base,Ref

class Image(Base):
    type = "image"
    fields = ['id', 'mime_type', 'description', 'location_prefix', 'intent']

    THUMB = 'thumb'
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'

    def __init__(self, **data):
        super(Image, self).__init__(**data)

    def _update_from_data(self, data):
        super(Image, self)._update_from_data(data)
        self.parent = Ref(**data.get('parent', {}))

    def image_url(self, protocol, size):
        return '{0}://{1}/{2}/{3}/{4}/{5}'.format(protocol, self.location_prefix, self.parent.ref_type, self.parent.identifier, size, self.identifier)

    def serialize_to_dictionary(self, with_refs=True):
        obj = super(Image, self).serialize_to_dictionary(with_refs)
        obj['parent'] = self.parent.serialize_to_dictionary(with_refs)
        return obj
