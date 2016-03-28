""" DataPipeline Parameters. """


from . import base


__all__ = [
    'String',
    'Integer',
    'Double',
    'AwsS3ObjectKey']


class String(base.TypedDataPipelineParameter): pass


class Integer(base.TypedDataPipelineParameter): pass


class Double(base.TypedDataPipelineParameter): pass


class AwsS3ObjectKey(base.TypedDataPipelineParameter):
    TYPE_NAME = 'AWS::S3::ObjectKey'
