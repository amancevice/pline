from .base import DataPipelineObject, TypedDataPipelineObject, Schedule
from .actions import SnsAlarm, Terminate
from .activities import CopyActivity, EmrActivity, HiveActivity, HiveCopyActivity, \
    PigActivity, RedshiftCopyActivity, ShellCommandActivity, SqlActivity, \
    ShellCommand
from .data_formats import CSV, Custom, DynamoDBDataFormat, DynamoDBExportDataFormat, \
    RegEx, TSV
from .data_nodes import DynamoDBDataNode, MySqlDataNode, RedshiftDataNode, S3DataNode, \
    SqlDataNode
from .databases import JdbcDatabase, RdsDatabase, RedshiftDatabase
from .pipeline import Pipeline
from .preconditons import DynamoDBDataExists, DynamoDBTableExists, Exists, S3KeyExists, \
    S3PrefixNotEmpty, ShellCommandPrecondition
from .resources import Ec2Resource, EmrCluster

# Constants

class _StringConstant(dict):
    def __init__(self, *args):
        for k in args:
            self[k] = k

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            super(DataPipelineObject, self).__getattr__(key)


failureAndRerunMode     = _StringConstant('CASCADE', 'NONE')
scheduleType            = _StringConstant('timeseries', 'cron')
startAt                 = _StringConstant('FIRST_ACTIVATION_DATE_TIME')
actionOnTaskFailure     = _StringConstant('continue', 'terminate')
actionOnResourceFailure = _StringConstant('retryAll', 'retryNone')
