from . import base, keywords

class Activity(base.RunnableObject): pass

class CopyActivity(Activity): pass


class EmrActivity(Activity): pass


class HiveActivity(Activity): pass


class HiveCopyActivity(Activity): pass


class PigActivity(Activity): pass


class RedshiftCopyActivity(Activity): pass


class ShellCommandActivity(Activity): pass


class SqlActivity(Activity): pass


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