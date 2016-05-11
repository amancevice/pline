""" DataPipeline Base. """


import collections
import itertools


class DataPipelineBase(collections.Iterable):
    def __init__(self, **kwargs):
        self._items = dict()
        for key, val in kwargs.iteritems():
            setattr(self, key, val)

    def __iter__(self):
        raise NotImplementedError

    def __getitem__(self, key):
        try:
            return getattr(self, key)
        except AttributeError:
            return self._items[key]

    def __len__(self):
        return len(self._items)


class DataPipelineParameter(DataPipelineBase):
    def __init__(self, **attributes):
        assert 'id'    in attributes, "'id' not in attributes"
        assert 'value' in attributes, "'value' not in attributes"
        self.id    = attributes['id']
        self.value = attributes['value']
        del attributes['id']
        del attributes['value']
        super(DataPipelineParameter, self).__init__(**attributes)

    def __repr__(self):
        return "<%s id: \"%s\", value: \"%s\">" % \
            (type(self).__name__, self.id, self.value)

    def __setattr__(self, key, value):
        if key not in ('id', 'value', '_items'):
            self.attributes[key] = value
        super(DataPipelineParameter, self).__setattr__(key, value)

    def __iter__(self):
        iterhelper = lambda kv: { 'key' : kv[0], 'stringValue' : str(kv[-1]) }
        yield 'id',          self.id
        yield 'stringValue', self.value
        yield 'attributes',  list(map(iterhelper, self.attributes.iteritems()))

    @property
    def attributes(self):
        return self._items


class TypedDataPipelineParameter(DataPipelineParameter):
    def __init__(self, **attributes):
        type_ = getattr(self, 'TYPE_NAME', type(self).__name__)
        attributes.setdefault('type', type_)
        super(TypedDataPipelineParameter, self).__init__(**attributes)


class DataPipelineObject(DataPipelineBase):
    def __init__(self, **fields):
        assert 'id'   in fields, "'id' not in fields"
        assert 'name' in fields, "'value' not in fields"
        self.id   = fields['id']
        self.name = fields['name']
        del fields['id']
        del fields['name']
        super(DataPipelineObject, self).__init__(**fields)

    def __repr__(self):
        return "<%s id: \"%s\", name: \"%s\">" % \
            (type(self).__name__, self.id, self.name)

    def __setattr__(self, key, value):
        if key not in ('id', 'name', '_items'):
            self.fields[key] = value
        super(DataPipelineObject, self).__setattr__(key, value)

    def __iter__(self):

        def iterhelper(keyvalue):
            key, value = keyvalue
            if isinstance(value, list):
                for val in value:
                    for item in iterhelper((key, val)):
                        yield item
            elif isinstance(value, DataPipelineObject):
                yield { 'key' : key, 'refValue' : value.id }
            elif isinstance(value, DataPipelineParameter):
                yield { 'key' : key, 'stringValue' : "#{%s}" % value.id }
            elif isinstance(value, bool):
                yield { 'key' : key, 'stringValue' : str(value).lower() }
            elif value is not None:
                yield { 'key' : key, 'stringValue' : str(value) }

        yield 'id',     self.id
        yield 'name',   self.name
        yield 'fields', list(itertools.chain(*map(iterhelper, self.fields.iteritems())))

    @property
    def fields(self):
        try:
            return self._items
        except AttributeError:
            self._items = dict()
            return self._items


class TypedDataPipelineObject(DataPipelineObject):
    def __init__(self, **fields):
        type_ = getattr(self, 'TYPE_NAME', type(self).__name__)
        fields.setdefault('type', type_)
        super(TypedDataPipelineObject, self).__init__(**fields)


class Schedule(TypedDataPipelineObject): pass


class RunnableObject(TypedDataPipelineObject): pass
