# pline

AWS Pipeline Wrapper for boto. Construct a Data Pipeline using Python objects.

Last updated: `0.0.2`

## Installation

```
pip install pline
```

## Simple usage

Create a pipeline object

```python

pipeline = pline.Pipeline(
    name      = 'MyPipeline',
    unique_id = 'MyPipeline1',
    desc      = 'An example',
    region    = 'us-west-2' )
```

The pipeline will connect to AWS automatically if you have set your AWS credentials at the
environmental level. If you want to connect using a specific configuration:

```python
pipeline.connect(
    aws_access_key_id        = 'my_access_key',
    aws_secret_access_key_id = 'my_secret_key' )
```

Create a schedule object

```python
schedule = pline.Schedule(
    name        = 'Schedule',
    id          = 'Schedule1',
    period      = '1 day',
    occurrences = 1 )
```

Create the default pipeline definition. The pipeline object has a helper-method to
create this object with sensible defaults:

```python
definition = pipeline.definition( schedule,
    pipelineLogUri = "s3://bucket/pipeline/log" )
```

Create an EC2 resource on which the pipeline will run

```python
resource = pline.Ec2Resource(
    name         = 'Resource',
    id           = 'Resource1',
    role         = 'DataPipelineDefaultRole',
    resourceRole = 'DataPipelineDefaultResourceRole',
    schedule     = schedule )
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

Add the schedule, definition, resource, and activity to the pipeline

```python
pipeline.add(schedule, definition, resource, activity)
```

Create the pipeline in AWS

```python
pipeline.create()
```

Create a new object, asscociate it with an existing object and add it to the pipeline

```python
sns_alarm = pline.SnsAlarm(
    name     = 'SnsAlarm',
    id       = 'SnsAlarm1',
    topicArn = 'arn:aws:sns:us-east-1:12345678abcd:my-arn',
    role     = 'DataPipelineDefaultRole' )
activity.onFailure = sns_alarm
pipeline.add(sns_alarm)
```

Update the pipeline on AWS and activate it

```python
pipeline.update()
pipeline.activate()
```
