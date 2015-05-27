from . import base

class DynamoDBDataExists(base.TypedDataPipelineObject): pass


class DynamoDBTableExists(base.TypedDataPipelineObject): pass


class Exists(base.TypedDataPipelineObject): pass


class S3KeyExists(base.TypedDataPipelineObject): pass


class S3PrefixNotEmpty(base.TypedDataPipelineObject): pass


class ShellCommandPrecondition(base.TypedDataPipelineObject): pass
