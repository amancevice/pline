""" DataPipeline Utils. """


__all__ = ['ShellCommand']


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
        for arg in args:
            self._commands.append(arg)
