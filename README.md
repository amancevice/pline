# pline Python library

<img src="https://travis-ci.org/amancevice/pline.svg?branch=master"/>

AWS Data Pipeline Wrapper for `boto3`. Construct a Data Pipeline using Python objects.

Last updated: `0.4.2`

## Installation

```
pip install pline
```

## Overview

The payload `boto3` requires for a pipeline definition is somewhat complex. This library 
provides the tools to model your pipeline using Python objects and transform the payload
into the expected data structure.

```python
import pline

my_activity = pline.activities.ShellCommandActivity(
    name='MyActivity', id='Activity_adbc1234')
my_activity.command = "echo $1 $2"
my_activity.scriptArgument = ['hello', 'world']

dict(my_activity)
{ 'id'     : 'Activity_adbc1234',
  'name'   : 'MyActivity',
  'fields' : [ {'key': 'command',        'stringValue': 'echo $1 $2'},
               {'key': 'type',           'stringValue': 'ShellCommandActivity'},
               {'key': 'scriptArgument', 'stringValue': 'hello'},
               {'key': 'scriptArgument', 'stringValue': 'world'} ]}
 ```

#### Data Pipeline Objects

Every object in a pipeline is an acestor of the `DataPipelineObject` class. Each object 
owns three key attributes:

* `name`
* `id`
* `fields`

The `name` and `id` attributes must be set at initialization time, but `fields` is 
handled internally by the object and should not be accessed directly.

Setting an object's attribute can be done via the initialization call or after the fact:

```python
node = pline.data_nodes.S3DataNode(
    id='MyDataNode1', name='MyDataNode1', workerGroup='TestGroup')
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

#### Data Pipeline Parameters

As of `0.2.0`, `pline` supports passing parameters to data pipelines. Parameters can be added to the 
pipeline and passed into `DataPipelineObject` instances.

```python
my_param = pline.parameters.String(
    id = 'MyParam1',
    value = 'Here is the value I am using',
    description = 'This value is extremely important',
    watermark = 'Choose a value between 0 and 99.')
```

#### Typed Data Pipeline Objects/Parameters

Most objects in a data pipeline are typed -- that is, they are given a `type` attribute on initialization
that is added to the `fields` attribute. By default, the type is taken from the name of the class (which
corresponds to the type given by AWS' specs).

Custom classes can override this behavior by defining a `TYPE_NAME` class-level attribute:

```python
class MyCustomS3DataNode(pline.S3DataNode):
    TYPE_NAME = 'S3DataNode'
    # ...

class MyCustomParam(pline.AwsS3ObjectKey):
    TYPE_NAME = 'AwsS3ObjectKey'
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
    aws_access_key_id     = 'my_access_key',
    aws_secret_access_key = 'my_secret_key' )
```

#### Create a schedule object

```python
schedule = pline.Schedule(
    id          = 'Schedule1',
    name        = 'Schedule',
    period      = '1 day',
    startAt     = pline.keywords.startAt.FIRST_ACTIVATION_DATE_TIME,
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
resource = pline.resources.Ec2Resource(
    id           = 'Resource1',
    name         = 'Resource',
    role         = 'DataPipelineDefaultRole',
    resourceRole = 'DataPipelineDefaultResourceRole',
    schedule     = schedule )
```

#### Create an activity

```python
activity = pline.activities.ShellCommandActivity(
    id       = 'MyActivity1',
    name     = 'MyActivity',
    runsOn   = resource,
    schedule = schedule,
    command  = 'echo hello world' )
```


#### Create a parameterized activity and its parameter

```python
param = pline.parameters.String(
    id          = 'myShellCmd',
    value       = 'grep -rc "GET" ${INPUT1_STAGING_DIR}/* > ${OUTPUT1_STAGING_DIR}/output.txt',
    description = 'Shell command to run' )

param_activity = pline.activities.ShellCommandActivity(
    id       = 'MyParamActivity1',
    name     = 'MyParamActivity1',
    runsOn   = resource,
    schedule = schedule,
    command  = param )
```

#### Add the objects to the pipeline

```python
pipeline.add(schedule, definition, resource, activity, param_activity)
```

#### Add the parameters to the pipeline

```python
pipeline.add_param(param)
```

#### View the pipeline definition payload

```python
print pipeline.payload()
```

#### Validate the pipeline definiton

```python
pipeline.validate()
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
sns_alarm = pline.actions.SnsAlarm(
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
cmd = pline.utils.ShellCommand(
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
