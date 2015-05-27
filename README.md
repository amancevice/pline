# pline

AWS Pipeline Wrapper for boto. Construct a Data Pipeline using Python objects.

Last updated: `0.0.2`

## Installation

```
pip install pline
```

## Simple usage

Create a schedule

```python
schedule = pline.Schedule(
    name        = 'Schedule',
    id          = 'Schedule1',
    startAt     = pline.startAt.FIRST_ACTIVATION_DATE_TIME,
    period      = '1 day',
    occurrences = 1 )
```

Create the default pipeline definition

```python
definition = pline.DataPipelineObject(
    name                = 'Default',
    id                  = 'Default',
    scheduleType        = pline.scheduleType.cron,
    failureAndRerunMode = pline.failureAndRerunMode.CASCADE,
    pipelineLogUri      = 's3://bucket/pipeline/log',
    role                = 'DataPipelineDefaultRole',
    resourceRole        = 'DataPipelineDefaultResourceRole' ,
    schedule            = schedule )
```

Create an EC2 resource on which the pipeline will run

```python
resource = pline.Ec2Resource(
    name                    = 'ec2-resource',
    id                      = 'ec2-resource',
    actionOnTaskFailure     = pline.actionOnTaskFailure.terminate,
    actionOnResourceFailure = pline.actionOnResourceFailure.retryAll,
    maximumRetries          = 1,
    terminateAfter          = '4 hours',
    imageId                 = 'ami-1234abcd',
    keyPair                 = 'my-keypair',
    role                    = 'DataPipelineDefaultRole',
    resourceRole            = 'DataPipelineDefaultResourceRole',
    subnetId                = 'subnet-abcd1234',
    securityGroupIds        = 'my-sg',
    schedule                = schedule )
```

Create an activity to run

```python
activity = pline.ShellCommandActivity(
    name     = 'MyActivity',
    id       = 'MyActivity1',
    runsOn   = resource,
    schedule = schedule,
    command  = 'echo hello world' )
```

Create and activate the pipeline

```python
pipeline = pline.Pipeline(
    name = 'MyPipeline',
    id   = 'MyPipeline1',
    desc = 'An example',
    region='us-west-2' )
pipeline.add(schedule, definition, resource, activity)
pipeline.create()
pipeline.activate()
```
