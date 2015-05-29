# pline Python library

AWS Pipeline Wrapper for `boto`. Construct a Data Pipeline using Python objects.

Last updated: `0.1.0`

## Installation

```
pip install pline
```

## What is it?

The payload `boto` requires for a pipeline definition is somewhat complex. This library 
provides the tools to model your pipeline as Python objects and wraps calls to `boto` 
that transform the payload into the proper format behind the scenes.

#### DataPipelineObject base class

Every object in a pipeline is an acestor of the `DataPipelineObject` class. Each object 
owns three key attributes:

* `name`
* `id`
* `fields`

The `name` and `id` attributes must be set at initialization time, but `fields` is 
handled internally by the object and should not be accessed directly.

Setting an object's attribute can be done via the initialization call or after the fact:

```python
node = pline.S3DataNode('MyDataNode1', 'MyDataNode1', workerGroup='TestGroup')
# => <S3DataNode name: "MyDataNode1", id: "MyDataNode1">
node.directoryPath = 's3://bucket/pipeline/'
print node.workerGroup
# => 'TestGroup'
print node.directoryPath
# => 's3://bucket/pipeline/'
```

`Pipeline` instances handle the conversion of pipeline objects to a payload, but objects can
be viewed in `boto`-friendly format by converting them to a `dict`:

```python
dict(node)
{ 'name'   : 'MyDataNode1',
  'id'     : 'MyDataNode1',
  'fields' : [
    { 'key' : 'type',          'stringValue' : 'S3DataNode' },
    { 'key' : 'directoryPath', 'stringValue' : 's3://bucket/pipeline/' },
    { 'key' : 'workerGroup',   'stringValue' : 'TestGroup' }, ] }
```

#### Typed DataPipelineObjects

Most objects in a data pipeline are typed -- that is, they are given a `type` attribute on initialization
that is added to the `fields` attribute. By default, the type is taken from the name of the class (which
corresponds to the type given by AWS' specs).

Custom classes can override this behavior by defining a `TYPE_NAME` class-level attribute:

```python
class MyCustomS3DataNode(pline.S3DataNode):
    TYPE_NAME = 'S3DataNode'
    # ...
```

## Example Pipeline

#### Create a pipeline object

```python

pipeline = pline.Pipeline(
    name      = 'MyPipeline',
    unique_id = 'MyPipeline1',
    desc      = 'An example pipeline description',
    region    = 'us-west-2' )
```

#### Connect (optional)

The pipeline will connect to AWS automatically if you have your AWS credentials set at
the environmental level. If you want to connect using a specific configuration:

```python
pipeline.connect(
    aws_access_key_id        = 'my_access_key',
    aws_secret_access_key_id = 'my_secret_key' )
```

#### Create a schedule object

```python
schedule = pline.Schedule(
    name        = 'Schedule',
    id          = 'Schedule1',
    period      = '1 day',
    startAt     = pline.startAt.FIRST_ACTIVATION_DATE_TIME,
    occurrences = 1 )
```

#### Create the default pipeline definition 

The pipeline object has a helper-method to create this object with sensible defaults:

```python
definition = pipeline.definition( schedule,
    pipelineLogUri = "s3://bucket/pipeline/log" )
```

#### Create an EC2 resource

This will be the machine running the tasks.

```python
resource = pline.Ec2Resource(
    name         = 'Resource',
    id           = 'Resource1',
    role         = 'DataPipelineDefaultRole',
    resourceRole = 'DataPipelineDefaultResourceRole',
    schedule     = schedule )
```

#### Create an activity

```python
activity = pline.ShellCommandActivity(
    name     = 'MyActivity',
    id       = 'MyActivity1',
    runsOn   = resource,
    schedule = schedule,
    command  = 'echo hello world' )
```

#### Add the objects to the pipeline

```python
pipeline.add(schedule, definition, resource, activity)
```

#### Create the pipeline in AWS

This will send the request to create a pipeline through boto

```python
pipeline.create()
```

#### Adding new objects to the pipeline

Sometimes you may want to add an object to the pipeline after it has been created

```python
# Add an alert
sns_alarm = pline.SnsAlarm(
    name     = 'SnsAlarm',
    id       = 'SnsAlarm1',
    topicArn = 'arn:aws:sns:us-east-1:12345678abcd:my-arn',
    role     = 'DataPipelineDefaultRole' )

# Associate it with the activity
activity.onFailure = sns_alarm

# Add it to the pipeline
pipeline.add(sns_alarm)
```

Update the pipeline on AWS and activate it

```python
pipeline.update()
pipeline.activate()
```

## ShellCommand helper

The `ShellCommand` class can be used to compose chained commands

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
