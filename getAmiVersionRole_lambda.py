#!/usr/bin/python
from __future__ import print_function
import boto3


def getAmiForVersionRole(role, version = None):
    ec2client = boto3.client('ec2')
    filters = [{'Name':'tag:imh:role', 'Values':[role]}]
    if version:
        filters += [{'Name':'tag:imh:version', 'Values':[version]}]
    targetAmi = ec2client.describe_images(
           Filters = filters
    )
    if targetAmi and len(targetAmi['Images']) and not role:
        return Exception('No AMI found for version: {0}'.format(version))
    return targetAmi


def extractVersion(targetAmi):
    version = ''
    for key, value in targetAmi.iteritems():
        if key == 'Images':
            for item in value:
                for element in item['Tags']:
                    if element['Key'] == 'imh:version':
                        version = element['Value']
    return version

def extractData(targetAmi, version):
    versionToImageId = {}
    versionList = []
    for key, value in targetAmi.iteritems():
        if key == 'Images':
            for item in value:
                versionToImageId['Name'] = version
                versionToImageId['Value'] = item['ImageId']
                versionList.append(versionToImageId)
    return versionList


def lambda_handler(event, context):
    #ami = getAmiForVersionRole(event['applicationVersion'], event['applicationRole'])
    ami = getAmiForVersionRole(event['role'], event['version'])
    version = extractVersion(ami)
    return extractData(ami, version)

#userVersion = '8.10.0-release-1'
#amiVersion = getAmiForVersionRole('hybris', userVersion)
#version = extractVersion(amiVersion)
#print('List Version: {0} \n\n'.format(extractData(amiVersion, version)))
