#!/usr/bin/python
# VERSION NOT ALWAYS GIVEN !!!!!!
import boto3


def getAmiForVersionRole(role, version = None):
    ec2client = boto3.client('ec2')
    filters = [{'Name':'tag:imh:role', 'Values':[role]}]
    if version:
        filters += [{'Name':'tag:imh:version', 'Values':['{0}*'.format(version)]}]
    targetAmi = ec2client.describe_images(
           Filters = filters
    )
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

def extractData(targetAmi):
    #Name = version, Value = AMI_ID
    #TODO: Get version from targetAmi
    currentTimestamp = 0
    previousTimestamp = 0
    for key, value in targetAmi.iteritems():
        if key == 'Images':
            for item in value:
                if item['CreationDate'] > currentTimestamp:
                    previousTimestamp = currentTimestamp
                    currentTimestamp = item['CreationDate']
                    #loop through and check version starts with development
    return timestampList

userVersion = 'development'
#amiVersion = getAmiForVersionRole('hybris', 'feature-WSP-786-4')
amiVersion = getAmiForVersionRole('hybris', userVersion)
print(amiVersion)
#version = extractVersion(amiVersion)
#print('List Version: {0} \n\n'.format(extractData(amiVersion, version)))
