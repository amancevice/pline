""" DataPipeline Databases. """


from . import base


__all__ = [
    'Database',
    'JdbcDatabase',
    'RdsDatabase',
    'RedshiftDatabase']


class Database(base.TypedDataPipelineObject): pass


class JdbcDatabase(Database): pass


class RdsDatabase(Database): pass


class RedshiftDatabase(Database): pass
