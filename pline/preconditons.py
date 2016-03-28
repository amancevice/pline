""" DataPipeline Preconditions. """


from . import base


__all__ = [
    'Precondition',
    'DynamoDBDataExists',
    'DynamoDBTableExists',
    'Exists',
    'S3KeyExists',
    'S3PrefixNotEmpty',
    'ShellCommandPrecondition']


class Precondition(base.TypedDataPipelineObject): pass


class DynamoDBDataExists(Precondition): pass


class DynamoDBTableExists(Precondition): pass


class Exists(Precondition): pass


class S3KeyExists(Precondition): pass


class S3PrefixNotEmpty(Precondition): pass


class ShellCommandPrecondition(Precondition): pass
