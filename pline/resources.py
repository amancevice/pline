""" DataPipeline Resources. """


from . import base


__all__ = [
    'Resource',
    'Ec2Resource',
    'EmrCluster']


class Resource(base.TypedDataPipelineObject): pass


class Ec2Resource(Resource): pass


class EmrCluster(Resource): pass
