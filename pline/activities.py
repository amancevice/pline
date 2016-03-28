""" DataPipeline Activities. """


from . import base


__all__ = [
    'Activity',
    'CopyActivity',
    'EmrActivity',
    'HiveActivity',
    'HiveCopyActivity',
    'PigActivity',
    'RedshiftCopyActivity',
    'ShellCommandActivity',
    'SqlActivity']


class Activity(base.RunnableObject): pass


class CopyActivity(Activity): pass


class EmrActivity(Activity): pass


class HiveActivity(Activity): pass


class HiveCopyActivity(Activity): pass


class PigActivity(Activity): pass


class RedshiftCopyActivity(Activity): pass


class ShellCommandActivity(Activity): pass


class SqlActivity(Activity): pass
