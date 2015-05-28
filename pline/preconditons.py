from . import base

class Precondition(base.TypedDataPipelineObject): pass


class DynamoDBDataExists(Precondition): pass


class DynamoDBTableExists(Precondition): pass


class Exists(Precondition): pass


class S3KeyExists(Precondition): pass


class S3PrefixNotEmpty(Precondition): pass


class ShellCommandPrecondition(Precondition): pass
