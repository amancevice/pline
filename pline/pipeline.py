__all__ = [ 'Pipeline' ]

import boto.datapipeline
import collections
import json
from . import base, keywords


class Pipeline(object):
    def __init__(self, name, unique_id, desc=None, region='us-east-1', pipeline_id=None):
        self.name        = name
        self.unique_id   = unique_id
        self.desc        = desc
        self.region_name = region
        self.pipeline_id = pipeline_id
        self.objects     = PipelineCollection()
        self.parameters  = PipelineCollection()

    @property
    def region(self):
        try:
            return self._region
        except AttributeError:
            self.connect()
            return self._region

    def payload(self, pipeline_id=None):
        """ Pipeline payload. """
        subdict = lambda dct,keys: { k:dct[k] for k in keys if k in dct }
        payload = {
            'pipelineId'       : pipeline_id or self.pipeline_id,
            'pipelineObjects'  : list(self.objects),
            'parameterValues'  : map(lambda x: subdict(x, ('id', 'stringValue')), self.parameters),
            'parameterObjects' : map(lambda x: subdict(x, ('id', 'attributes')), self.parameters) }

        return payload

    def definition(self, schedule,
        scheduleType        = keywords.scheduleType.cron,
        failureAndRerunMode = keywords.failureAndRerunMode.CASCADE,
        pipelineLogUri      = None,
        role                = 'DataPipelineDefaultRole',
        resourceRole        = 'DataPipelineDefaultResourceRole',
        **kwargs):
        """ Initialize the 'Default' pipeline definition object. """
        default = base.DataPipelineObject(
                        name                = 'Default',
                        id                  = 'Default',
                        scheduleType        = scheduleType,
                        failureAndRerunMode = failureAndRerunMode,
                        pipelineLogUri      = pipelineLogUri,
                        role                = role,
                        resourceRole        = resourceRole,
                        schedule            = schedule,
                        **kwargs )
        return default

    def connect(self, region_name=None, aws_access_key_id=None, aws_secret_access_key=None, **kwargs):
        """ Connect to AWS region.

            Arguments:
                region_name           (str):  Optional AWS region name
                aws_access_key_id     (str):  Optional AWS Access Key
                aws_secret_access_key (str):  Optional AWS Secret Key

            Returns:
                A handle to the boto connection. """
        region_name = region_name or self.region_name
        kwargs.setdefault('aws_access_key_id', aws_access_key_id)
        kwargs.setdefault('aws_secret_access_key', aws_secret_access_key)
        self._region = boto.datapipeline.connect_to_region(region_name, **kwargs)
        return self._region

    def activate(self):
        """ Activate pipeline. """
        assert self.pipeline_id is not None, "pipeline_id is None"
        return self.region.activate_pipeline(self.pipeline_id)

    def update(self):
        """ Update pipeline definition with self.objects. """
        assert self.pipeline_id is not None, "pipeline_id is None"
        payload = json.dumps(self.payload(self.pipeline_id))
        return self.region.make_request(action='PutPipelineDefinition', body=payload)

    def validate(self):
        """ Validate the pipeline definition. """
        assert self.pipeline_id is not None, "pipeline_id is None"
        payload = json.dumps(self.payload(self.pipeline_id))
        return self.region.make_request(action='ValidatePipelineDefinition', body=payload)

    def create(self):
        """ Create pipeline and set pipeline_id. """
        response = self.region.create_pipeline(self.name, self.unique_id, self.desc)
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
        map(self.add, items)

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
        try:
            return self._collection
        except AttributeError:
            self._collection = set()
            return self._collection
