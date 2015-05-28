from . import base

class Resource(base.TypedDataPipelineObject): pass


class Ec2Resource(Resource): pass


class EmrCluster(Resource): pass
