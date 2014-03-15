from _core import Base

class Asset(Base):
    fields = ['bitrate', 'codec', 'location', 'resource']
    refs = ['track']

    def __init__(self, **data):
        super(Asset, self).__init__(**data)