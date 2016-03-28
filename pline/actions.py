""" DataPipeline Actions. """


from . import base


__all__ = [
    'Action',
    'SnsAlarm',
    'Terminate']


class Action(base.TypedDataPipelineObject): pass


class SnsAlarm(Action): pass


class Terminate(Action): pass
