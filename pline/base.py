import itertools
from . import keywords

class DataPipelineObject(object):
    def __init__(self, *args, **kwargs):
        self.fields = dict()

        # Set name/id if given as args
        if len(args) == 1:
            setattr(self, 'name', str(args[0]))
        elif len(args) == 2:
            setattr(self, 'name', str(args[0]))
            setattr(self, 'id',   str(args[1]))
        elif len(args) > 2:
            raise TypeError("__init__() takes at most 3 arguments (%d given)" % (len(args)+1))

        # Set kwargs
        for k,v in kwargs.iteritems():
            setattr(self, k, v)

        # Ensure name/id set
        if self.name is None and self.id is None:
            raise TypeError("Both 'name' and 'id' keys must be supplied")
        elif self.name is None:
            raise TypeError("'name' key must be supplied")
        elif self.id is None:
            raise TypeError("'id' key must be supplied")

    def __iter__(self):
        def iterhelper(keyvalue):
            key, value = keyvalue
            if isinstance(value, list):
                map(iterhelper, [(key, x) for x in value])
            elif isinstance(value, DataPipelineObject):
                yield { 'key' : key, 'refValue' : value.id }
            elif isinstance(value, bool):
                yield { 'key' : key, 'stringValue' : str(value).lower() }
            else:
                yield { 'key' : key, 'stringValue' : str(value) }

        yield 'name',   self.name
        yield 'id',     self.id
        yield 'fields', list(itertools.chain(*map(iterhelper, self.fields.iteritems())))

    def __repr__(self):
        return "<%s name: \"%s\", id: \"%s\">" % (type(self).__name__, self.name, self.id)

    def __setattr__(self, key, value):
        if key not in ('id', 'name', 'fields'):
            self.fields[key] = value
        super(DataPipelineObject, self).__setattr__(key, value)


class TypedDataPipelineObject(DataPipelineObject):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('type', getattr(self, 'TYPE_NAME', type(self).__name__))
        super(TypedDataPipelineObject, self).__init__(*args, **kwargs)


class Schedule(TypedDataPipelineObject): pass


class RunnableObject(TypedDataPipelineObject): pass
