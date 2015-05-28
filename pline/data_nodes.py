from . import base, constants

class DataNode(base.RunnableObject):
    _defaults = { 'scheduleType' : constants.scheduleType.timeseries }


class DynamoDBDataNode(DataNode): pass


class MySqlDataNode(DataNode): pass


class RedshiftDataNode(DataNode): pass


class S3DataNode(DataNode):
    _defaults = { 's3EncryptionType' : constants.s3EncryptionType.SERVER_SIDE_ENCRYPTION }


class SqlDataNode(DataNode): pass