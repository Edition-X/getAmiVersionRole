#!/usr/bin/python
from __future__ import print_function

import boto3

def getAmiForVersion(version, role):
    ec2client = boto3.client('ec2')

    filters = [{'Name':'tag:imh:version', 'Values':[version]}]
    if role:
        filters += [{'Name':'tag:imh:role', 'Values':[role]}]
    targetAmi = ec2client.describe_images(
           Filters = filters
    )
    if targetAmi and len(targetAmi['Images'] and not role):
        return Exception('No AMI found for Version: {0}'.format(version))

    if targetAmi and len(targetAmi['Images'] and role):
        return Exception('No AMI found for Version: {0} and Role: {1}'.format(version, role))

def lambda_handler(event, context):
    cloudformation = boto3.resource('cloudformation')
    stack = cloudformation.Stack(event['stackname'])
    amiId = getAmiForVersion(event['applicationVersion'], event['applicationRole'])
    
    parameters = stack.parameters
    tags = stack.tags

    for i, param in enumerate(parameters):
        if parameters[i]['ParameterKey'] == 'HybrisserverAMI':
            parameters[i]['ParameterValue'] = amiId
    
    for i, tag in enumerate(tags):
        if tags[i]['Key'] == 'imh:stack:application-version':
            tags[i]['Value'] = event['applicationVersion']

    for i, tag in enumerate(tags):
        if tags[i]['Key'] == 'imh:stack:roles':
            tags[i]['Value'] = event['applicationRole']

    response = stack.update(
        UsePreviousTemplate=True,
        Parameters = parameters,
        Tags = tags,
    )
