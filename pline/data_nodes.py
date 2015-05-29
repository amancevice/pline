from . import base, keywords

class DataNode(base.RunnableObject): pass


class DynamoDBDataNode(DataNode): pass


class MySqlDataNode(DataNode): pass


class RedshiftDataNode(DataNode): pass


class S3DataNode(DataNode): pass


class SqlDataNode(DataNode): pass
