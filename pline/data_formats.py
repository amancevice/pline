""" DataPipeline Data Formats. """


from . import base


__all__ = [
    'DataFormat',
    'CSV',
    'Custom',
    'DynamoDBDataFormat',
    'DynamoDBExportDataFormat',
    'RegEx',
    'TSV']


class DataFormat(base.TypedDataPipelineObject): pass


class CSV(DataFormat): pass


class Custom(DataFormat): pass


class DynamoDBDataFormat(DataFormat): pass


class DynamoDBExportDataFormat(DataFormat): pass


class RegEx(DataFormat): pass


class TSV(DataFormat): pass
