# pline

AWS Pipeline Wrapper for boto. Construct a Data Pipeline using Python objects.

Last updated: `0.0.3`

## Installation

```
pip install pline
```

## Usage

Create a **pipeline** object

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

Create a **schedule** object

```python
schedule = pline.Schedule(
    name        = 'Schedule',
    id          = 'Schedule1',
    period      = '1 day',
    occurrences = 1 )
```

Create the **default pipeline definition**. The pipeline object has a helper-method to
create this object with sensible defaults:

```python
definition = pipeline.definition( schedule,
    pipelineLogUri = "s3://bucket/pipeline/log" )
```

Create an EC2 **resource** on which the pipeline will run

```python
resource = pline.Ec2Resource(
    name         = 'Resource',
    id           = 'Resource1',
    role         = 'DataPipelineDefaultRole',
    resourceRole = 'DataPipelineDefaultResourceRole',
    schedule     = schedule )
```

Create an **activity** to run

```python
activity = pline.ShellCommandActivity(
    name     = 'MyActivity',
    id       = 'MyActivity1',
    runsOn   = resource,
    schedule = schedule,
    command  = 'echo hello world' )
```

Add the **schedule**, **definition**, **resource**, and **activity** to the pipeline

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

## Advanced ShellCommandActivity use

The class `ShellCommand` can be used to compose chained commands

```python
cmd = pline.ShellCommand(
    'docker start registry',
    'sleep 3',
    'docker pull localhost:5000/my_docker',
    'docker stop registry' )
# => docker start registry;\
#    sleep 3;\
#    docker pull localhost:5000/my_docker;\
#    docker stop registry

cmd.append('echo all done')
# => docker start registry;\
#    sleep 3;\
#    docker pull localhost:5000/my_docker;\
#    docker stop registry;\
#    echo all done

activity.command = cmd
```

## Defaults

Defaults are applied as class-level attributes and are merged down the MRO line.

For example, the `S3DataNode` object inherits from: `DataNode`, and `RunnableObject`.
Each of these classes can define its own default attributes, but inherits any
higher-level attributes as well.

```python
pline.base.RunnableObject.defaults()
{ 'maximumRetries' : 2,
  'retryDelay'     : '10 minutes' }

pline.data_nodes.DataNode.defaults()
{ 'maximumRetries' : 2,
  'retryDelay'     : '10 minutes',
  'scheduleType'   : 'timeseries' }

pline.S3DataNode.defaults()
{ 'maximumRetries'   : 2,
  'retryDelay'       : '10 minutes',
  's3EncryptionType' : 'SERVER_SIDE_ENCRYPTION',
  'scheduleType'     : 'timeseries' }
```
