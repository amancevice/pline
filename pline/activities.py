from . import base

class CopyActivity(base.TypedDataPipelineObject): pass


class EmrActivity(base.TypedDataPipelineObject): pass


class HiveActivity(base.TypedDataPipelineObject): pass


class HiveCopyActivity(base.TypedDataPipelineObject): pass


class PigActivity(base.TypedDataPipelineObject): pass


class RedshiftCopyActivity(base.TypedDataPipelineObject): pass


class ShellCommandActivity(base.TypedDataPipelineObject): pass


class SqlActivity(base.TypedDataPipelineObject): pass


class ShellCommand(object):
    def __init__(self, *args):
        self._commands = list(args)

    def __repr__(self):
        if len(self._commands) == 1:
            return self._commands[0]
        return ";\\\n".join(self._commands)

    def __str__(self):
        return repr(self)

    def append(self, *args):
        map(self._commands.append, args)