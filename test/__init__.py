__author__ = 'amancevice'


import pline
from nose.tools import assert_equal, assert_dict_equal


def test_activity_shape():
    my_activity = pline.ShellCommandActivity(name='MyActivity', id='Activity_adbc1234')
    my_activity.command = "echo $1 $2"
    my_activity.scriptArgument = ['hello', 'world']

    returned = dict(my_activity)
    expected = {
        'id'     : 'Activity_adbc1234',
        'name'   : 'MyActivity',
        'fields' : [
            { 'key': 'command',        'stringValue': 'echo $1 $2' },
            { 'key': 'type',           'stringValue': 'ShellCommandActivity' },
            { 'key': 'scriptArgument', 'stringValue': 'hello' },
            { 'key': 'scriptArgument', 'stringValue': 'world' }]}
    assert_dict_equal(returned, expected)


def test_initattr():
    node     = pline.S3DataNode(id='MyDataNode1', name='MyDataNode1', workerGroup='TestGroup')
    returned = node.workerGroup
    expected = 'TestGroup'
    assert_equal(returned, expected)


def test_setattr():
    node = pline.S3DataNode(id='MyDataNode1', name='MyDataNode1', workerGroup='TestGroup')
    node.directoryPath = 's3://bucket/pipeline/'
    returned = node.directoryPath
    expected = 's3://bucket/pipeline/'
    assert_equal(returned, expected)


def test_node_shape():
    node = pline.S3DataNode(id='MyDataNode1', name='MyDataNode1', workerGroup='TestGroup')
    node.directoryPath = 's3://bucket/pipeline/'
    returned = dict(node)
    expected = {
        'id'     : 'MyDataNode1',
        'name'   : 'MyDataNode1',
        'fields' : [
            { 'stringValue' : 'TestGroup',             'key' : 'workerGroup' },
            { 'stringValue' : 's3://bucket/pipeline/', 'key' : 'directoryPath' },
            { 'stringValue' : 'S3DataNode',            'key' : 'type' }]}
    assert_dict_equal(returned, expected)


def test_param_shape():
    my_param = pline.String(
        id = 'MyParam1',
        value = 'Here is the value I am using',
        description = 'This value is extremely important',
        watermark = 'Choose a value between 0 and 99.')
    returned = dict(my_param)
    expected = {
        'id'          : 'MyParam1',
        'stringValue' : 'Here is the value I am using',
        'attributes'  : [
            { 'key': 'type', 'stringValue': 'String' },
            { 'key': 'description', 'stringValue': 'This value is extremely important' },
            { 'key': 'watermark', 'stringValue': 'Choose a value between 0 and 99.' }]}
    assert_dict_equal(returned, expected)


class MyCustomS3DataNode(pline.S3DataNode):
    TYPE_NAME = 'S3DataNode'


def test_custom_class_type():
    node = MyCustomS3DataNode(id='Foo', name='Bar')
    assert_equal(node.type, 'S3DataNode')


def test_pipeline_assembly():
    pipeline = pline.Pipeline(
        name      = 'MyPipeline',
        unique_id = 'MyPipeline1',
        desc      = 'An example pipeline description',
        region    = 'us-west-2' )

    schedule = pline.Schedule(
        id          = 'Schedule1',
        name        = 'Schedule',
        period      = '1 day',
        startAt     = pline.startAt.FIRST_ACTIVATION_DATE_TIME,
        occurrences = 1 )

    definition = pipeline.definition( schedule,
        pipelineLogUri = "s3://bucket/pipeline/log" )

    resource = pline.Ec2Resource(
        id           = 'Resource1',
        name         = 'Resource',
        role         = 'DataPipelineDefaultRole',
        resourceRole = 'DataPipelineDefaultResourceRole',
        schedule     = schedule )

    activity = pline.ShellCommandActivity(
        id       = 'MyActivity1',
        name     = 'MyActivity',
        runsOn   = resource,
        schedule = schedule,
        command  = 'echo hello world' )

    param = pline.String(
        id          = 'myShellCmd',
        value       = 'grep -rc "GET" ${INPUT1_STAGING_DIR}/* > ${OUTPUT1_STAGING_DIR}/output.txt',
        description = 'Shell command to run' )

    param_activity = pline.ShellCommandActivity(
        id       = 'MyParamActivity1',
        name     = 'MyParamActivity1',
        runsOn   = resource,
        schedule = schedule,
        command  = param )

    pipeline.add(schedule, definition, resource, activity, param_activity)

    pipeline.add_param(param)

    returned = pipeline.payload()
    expected = {
        'pipelineId'       : None,
        'parameterValues'  : [{'stringValue': 'grep -rc "GET" ${INPUT1_STAGING_DIR}/* > ${OUTPUT1_STAGING_DIR}/output.txt', 'id': 'myShellCmd'}],
        'parameterObjects' : [{'attributes': [{'stringValue': 'String', 'key': 'type'}, {'stringValue': 'Shell command to run', 'key': 'description'}], 'id': 'myShellCmd'}],
        'pipelineObjects'  : [{'fields': [{'stringValue': 'DataPipelineDefaultResourceRole', 'key': 'resourceRole'}, {'stringValue': 'DataPipelineDefaultRole', 'key': 'role'}, {'stringValue': 'Ec2Resource', 'key': 'type'}, {'refValue': 'Schedule1', 'key': 'schedule'}], 'id': 'Resource1', 'name': 'Resource'}, {'fields': [{'stringValue': '#{myShellCmd}', 'key': 'command'}, {'refValue': 'Schedule1', 'key': 'schedule'}, {'stringValue': 'ShellCommandActivity', 'key': 'type'}, {'refValue': 'Resource1', 'key': 'runsOn'}], 'id': 'MyParamActivity1', 'name': 'MyParamActivity1'}, {'fields': [{'stringValue': 'echo hello world', 'key': 'command'}, {'refValue': 'Schedule1', 'key': 'schedule'}, {'stringValue': 'ShellCommandActivity', 'key': 'type'}, {'refValue': 'Resource1', 'key': 'runsOn'}], 'id': 'MyActivity1', 'name': 'MyActivity'}, {'fields': [{'stringValue': 'FIRST_ACTIVATION_DATE_TIME', 'key': 'startAt'}, {'stringValue': 'Schedule', 'key': 'type'}, {'stringValue': '1 day', 'key': 'period'}, {'stringValue': '1', 'key': 'occurrences'}], 'id': 'Schedule1', 'name': 'Schedule'}, {'fields': [{'stringValue': 's3://bucket/pipeline/log', 'key': 'pipelineLogUri'}, {'refValue': 'Schedule1', 'key': 'schedule'}, {'stringValue': 'DataPipelineDefaultResourceRole', 'key': 'resourceRole'}, {'stringValue': 'CASCADE', 'key': 'failureAndRerunMode'}, {'stringValue': 'DataPipelineDefaultRole', 'key': 'role'}, {'stringValue': 'cron', 'key': 'scheduleType'}], 'id': 'Default', 'name': 'Default'}]}
    for i, val in enumerate(returned['parameterValues']):
        yield assert_dict_equal, val, expected['parameterValues'][i]
    for i, val in enumerate(returned['parameterObjects']):
        yield assert_dict_equal, val, expected['parameterObjects'][i]
    for i, val in enumerate(returned['pipelineObjects']):
        yield assert_equal, val['id'], expected['pipelineObjects'][i]['id']
        yield assert_equal, val['name'], expected['pipelineObjects'][i]['name']
        for j, field in enumerate(val['fields']):
            yield assert_dict_equal, field, expected['pipelineObjects'][i]['fields'][j]

    #assert_dict_equal(returned, expected)
