__all__ = [
    'Action',
    'SnsAlarm',
    'Terminate' ]


from . import base


class Action(base.TypedDataPipelineObject): pass


class SnsAlarm(Action): pass


class Terminate(Action): pass
