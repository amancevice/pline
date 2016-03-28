""" DataPipeline Data Nodes. """


from . import base


__all__ = [
    'DataNode',
    'DynamoDBDataNode',
    'MySqlDataNode',
    'RedshiftDataNode',
    'S3DataNode',
    'SqlDataNode']


class DataNode(base.RunnableObject): pass


class DynamoDBDataNode(DataNode): pass


class MySqlDataNode(DataNode): pass


class RedshiftDataNode(DataNode): pass


class S3DataNode(DataNode): pass


class SqlDataNode(DataNode): pass
