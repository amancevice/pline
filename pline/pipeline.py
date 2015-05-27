import boto.datapipeline

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

    def connect(self, **kwargs):
        """ Connect to AWS region. """
        return boto.datapipeline.connect_to_region(self.region_name, **kwargs)

    def activate(self, pipeline_id=None):
        """ Activate pipeline. """
        pipeline_id = pipeline_id or self.pipeline_id
        return self.region.activate_pipeline(pipeline_id)

    def update(self, pipeline_id=None):
        """ Update pipeline definition with self.objects. """
        pipeline_id = pipeline_id or self.pipeline_id
        return self.region.put_pipeline_definition(self.objects, pipeline_id)

    def create(self):
        """ Create pipeline and set pipeline_id. """
        pipeline = self.region.create_pipeline(self.name, self.unique_id, self.desc)
        self.pipeline_id = pipeline['pipelineId']
        self.update()
        return pipeline

    def add(self, *objects):
        """ Add pipeline objects to pipeline. """
        self.objects += objects
