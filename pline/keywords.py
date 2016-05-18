""" DataPipeline Keywords. """


__all__ = [
    'actionOnResourceFailure',
    'actionOnTaskFailure',
    'failureAndRerunMode',
    's3EncryptionType',
    'scheduleType',
    'startAt']


def _keywords(*values):
    return type('KEYWORD', (), dict([('__slots__', values)] + [(v,v) for v in values]))


actionOnResourceFailure = _keywords('retryAll', 'retryNone')
actionOnTaskFailure     = _keywords('continue', 'terminate')
failureAndRerunMode     = _keywords('CASCADE', 'NONE')
s3EncryptionType        = _keywords('SERVER_SIDE_ENCRYPTION', 'NONE')
scheduleType            = _keywords('timeseries', 'cron', 'ondemand')
startAt                 = _keywords('FIRST_ACTIVATION_DATE_TIME')
