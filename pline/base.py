from . import constants

class DataPipelineObject(dict):
    _defaults = dict()

    def __init__(self, *args, **kwargs):
        self['fields'] = list()

        # Set defalts
        for k,v in self.defaults().iteritems():
            if k not in kwargs:
                setattr(self, k, v)

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

        # Ensure name/id in self
        if 'name' not in self and 'id' not in self:
            raise KeyError("Both 'name' and 'id' keys must be supplied")
        elif 'name' not in self:
            raise KeyError("'name' key must be supplied")
        elif 'id' not in self:
            raise KeyError("'id' key must be supplied")

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

    @classmethod
    def defaults(cls):
        return { k:v for x in reversed(cls.mro()[:-2]) for k,v in x._defaults.items() }


class TypedDataPipelineObject(DataPipelineObject):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('type', type(self).__name__)
        super(TypedDataPipelineObject, self).__init__(*args, **kwargs)


class Schedule(TypedDataPipelineObject):
    _defaults = { 'id'      : 'DefaultSchedule',
                 'startAt' : constants.startAt.FIRST_ACTIVATION_DATE_TIME }


class RunnableObject(TypedDataPipelineObject):
    _defaults = { 'maximumRetries' : 2,
                  'retryDelay'     : '10 minutes' }