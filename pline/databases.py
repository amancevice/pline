from . import base

class Database(base.TypedDataPipelineObject): pass


class JdbcDatabase(Database): pass


class RdsDatabase(Database): pass


class RedshiftDatabase(Database): pass
