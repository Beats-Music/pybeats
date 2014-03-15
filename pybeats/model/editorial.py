from pybeats.api import BeatsAPI
from _core import Base, Ref

class Bio(Base):
    type = "bio"
    fields = ['length', 'content']

    SHORT = 'short'
    LONG = 'long'

    def __init__(self, **data):
        super(Bio, self).__init__(**data)

    def _update_from_data(self, data):
        super(Bio, self)._update_from_data(data)
        self.subject = Ref(**data.get('subject', {}))

    def serialize_to_dictionary(self, with_refs=True):
        obj = super(Bio, self).serialize_to_dictionary(with_refs)
        obj['subject'] = self.parent.serialize_to_dictionary(with_refs)
        return obj

class Review(Base):
    type = "review"
    fields = ['rating', 'content', 'source', 'author', 'headline']

    def __init__(self, **data):
        super(Review, self).__init__(**data)

    def _update_from_data(self, data):
        super(Review, self)._update_from_data(data)
        self.subject = Ref(**data.get('subject', {}))

    def serialize_to_dictionary(self, with_refs=True):
        obj = super(Review, self).serialize_to_dictionary(with_refs)
        obj['subject'] = self.parent.serialize_to_dictionary(with_refs)
        return obj

class Recommendation(Base):
    type = "recommendation"
    fields = ['blurb']

    def __init__(self, **data):
        super(Recommendation, self).__init__(**data)

    def _update_from_data(self, data):
        super(Recommendation, self)._update_from_data(data)
        content = data.get('content', {})
        cls = Base.class_for_type(content.get('type', ''))
        self.content = cls(**content)

    def serialize_to_dictionary(self, with_refs=True):
        obj = super(Recommendation, self).serialize_to_dictionary(with_refs)
        obj['content'] = self.content.serialize_to_dictionary(with_refs)
        return obj
