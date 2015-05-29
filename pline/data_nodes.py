from . import base, keywords

class DataNode(base.RunnableObject):
    _defaults = { 'scheduleType' : keywords.scheduleType.timeseries }


class DynamoDBDataNode(DataNode): pass


class MySqlDataNode(DataNode): pass


class RedshiftDataNode(DataNode): pass


class S3DataNode(DataNode):
    _defaults = { 's3EncryptionType' : keywords.s3EncryptionType.SERVER_SIDE_ENCRYPTION }


class SqlDataNode(DataNode): pass
