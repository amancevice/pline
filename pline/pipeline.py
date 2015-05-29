import boto.datapipeline
from . import base, keywords

class Pipeline(object):
    def __init__(self, name, unique_id, desc=None, region='us-east-1', pipeline_id=None):
        self.name        = name
        self.unique_id   = unique_id
        self.desc        = desc
        self.region_name = region
        self.pipeline_id = pipeline_id
        self.objects     = list()

    @property
    def region(self):
        try:
            return self._region
        except AttributeError:
            self._region = self.connect()
            return self._region

    def definition(self, schedule,
        scheduleType        = keywords.scheduleType.cron,
        failureAndRerunMode = keywords.failureAndRerunMode.CASCADE,
        pipelineLogUri      = None,
        role                = 'DataPipelineDefaultRole',
        resourceRole        = 'DataPipelineDefaultResourceRole',
        **kwargs):
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
        return boto.datapipeline.connect_to_region(region_name, **kwargs)

    def activate(self, pipeline_id=None):
        """ Activate pipeline.

            Arguments:
                pipeline_id (str):  Optional ID of pipeline if called without create()

            Returns:
                boto response. """
        pipeline_id = pipeline_id or self.pipeline_id
        return self.region.activate_pipeline(pipeline_id)

    def update(self, pipeline_id=None):
        """ Update pipeline definition with self.objects.

            Arguments:
                pipeline_id (str):  Optional ID of pipeline if called without create()

            Returns:
                boto response. """
        pipeline_id = pipeline_id or self.pipeline_id
        objects = map(dict, self.objects)
        return self.region.put_pipeline_definition(objects, pipeline_id)

    def create(self):
        """ Create pipeline and set pipeline_id. """
        response = self.region.create_pipeline(self.name, self.unique_id, self.desc)
        self.pipeline_id = response['pipelineId']
        if any(self.objects):
            self.update()
        return response

    def add(self, *objects):
        """ Add pipeline objects to pipeline. """
        self.objects += objects
