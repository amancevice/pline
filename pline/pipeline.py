""" DataPipeline. """


import collections
import boto3
import botocore
from . import base, exceptions, keywords


__all__ = ['Pipeline']


class Pipeline(object):
    def __init__(self, name, unique_id, desc=None, region='us-east-1', pipeline_id=None):
        self.name        = name
        self.unique_id   = unique_id
        self.desc        = desc
        self.region_name = region
        self.pipeline_id = pipeline_id
        self.objects     = PipelineCollection()
        self.parameters  = PipelineCollection()
        self._client     = None

    @property
    def client(self):
        if self._client is None:
            self.connect()
        return self._client

    def payload(self, pipeline_id=None):
        """ Pipeline payload. """
        subdict = lambda dct,keys: { k:dct[k] for k in keys if k in dct }
        values  = lambda x: subdict(x, ('id', 'stringValue'))
        objects = lambda x: subdict(x, ('id', 'attributes'))
        return {
            'pipelineId'       : pipeline_id or self.pipeline_id,
            'pipelineObjects'  : list(self.objects),
            'parameterValues'  : map(values, self.parameters),
            'parameterObjects' : map(objects, self.parameters) }

    @staticmethod
    def definition(schedule, **kwargs):
        """ Initialize the 'Default' pipeline definition object. """
        kwargs.setdefault('scheduleType',        keywords.scheduleType.cron)
        kwargs.setdefault('failureAndRerunMode', keywords.failureAndRerunMode.CASCADE)
        kwargs.setdefault('role',                'DataPipelineDefaultRole')
        kwargs.setdefault('resourceRole',        'DataPipelineDefaultResourceRole')
        kwargs['schedule'] = schedule
        return base.DataPipelineObject(name='Default', id='Default', **kwargs)

    def connect(self, *args, **kwargs):
        """ Connect to AWS region.

            Arguments:
                args   (tuple): Arguments to pass to boto3.client() after 'datapipeline'
                kwargs (dict):  Keyword arguments to pass to boto3.client()
                                excluding service_name='datapipeline'

            Returns:
                A handle to the boto connection. """
        kwargs.setdefault('region_name', self.region_name)
        self._client = boto3.client('datapipeline', *args, **kwargs)
        return self._client

    def activate(self, **kwargs):
        """ Activate pipeline. """
        assert self.pipeline_id is not None, "pipeline_id is None"
        try:
            return self.client.activate_pipeline(pipelineId=self.pipeline_id, **kwargs)
        except botocore.exceptions.ClientError as err:
            raise exceptions.ClientError(err)

    def update(self):
        """ Update pipeline definition with self.objects. """
        assert self.pipeline_id is not None, "pipeline_id is None"
        try:
            return self.client.put_pipeline_definition(**self.payload())
        except botocore.exceptions.ClientError as err:
            raise exceptions.ClientError(err)

    def validate(self):
        """ Validate the pipeline definition. """
        assert self.pipeline_id is not None, "pipeline_id is None"
        try:
            return self.client.validate_pipeline_definition(**self.payload())
        except botocore.exceptions.ClientError as err:
            raise exceptions.ClientError(err)

    def create(self):
        """ Create pipeline and set pipeline_id. """
        try:
            response = self.client.create_pipeline(
                name        = self.name,
                uniqueId    = self.unique_id,
                description = self.desc)
        except botocore.exceptions.ClientError as err:
            raise exceptions.ClientError(err)
        self.pipeline_id = response['pipelineId']
        if any(self.objects) or any(self.parameters):
            self.update()
        return response

    def add(self, *objects):
        """ Add an object to the pipeline. """
        return self.objects.add(*objects)

    def add_param(self, *params):
        """ Add a parameter to the pipeline. """
        return self.parameters.add(*params)


class PipelineCollection(collections.MutableSet):
    def __init__(self, *items):
        self._collection = set()
        for item in items:
            self.add(item)

    def __contains__(self, item):
        return item in self.collection

    def __iter__(self):
        return iter(map(dict, self.collection))

    def __len__(self):
        return len(self.collection)

    def add(self, *items):
        """ Add one or more items to the collection. """
        for item in items:
            self.collection.add(item)

    def discard(self, *items):
        """ Discard one or more items from the collection. """
        for item in items:
            self.collection.discard(item)

    @property
    def collection(self):
        """ Collection component. """
        return self._collection
