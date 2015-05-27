class DataPipelineObject(dict):
    def __init__(self, name, id, **kwargs):
        self['name']   = name
        self['id']     = id
        self['fields'] = list()
        for k,v in kwargs.iteritems():
            setattr(self, k, v)

    def __setattr__(self, key, value):
        if key in ('id', 'name'):
            self[key] = value
        elif isinstance(value, DataPipelineObject):
            self['fields'].append({ 'key' : key, 'refValue' : value.id })
        elif isinstance(value, bool):
            self['fields'].append({ 'key' : key, 'stringValue' : str(value).lower() })
        elif isinstance(value, list):
            for item in value:
                self.__setattr__(key, item)
        else:
            self['fields'].append({ 'key' : key, 'stringValue' : str(value) })
        super(DataPipelineObject, self).__setattr__(key, value)

    def __getattr__(self, key):
        try:
            if key in ('id', 'name'):
                return self[key]
            return iter(x for x in self['fields'] if x['key'] == key).next()
        except StopIteration:
            super(DataPipelineObject, self).__getattr__(key)


class TypedDataPipelineObject(DataPipelineObject):
    def __init__(self, name, id, **kwargs):
        kwargs.setdefault('type', type(self).__name__)
        super(TypedDataPipelineObject, self).__init__(name, id, **kwargs)


class Schedule(TypedDataPipelineObject): pass
