#!/usr/bin/python
import boto3


def getAmiForVersionRole(role, version = None):
    ec2client = boto3.client('ec2')
    filters = [{'Name':'tag:imh:role', 'Values':[role]}]
    if version:
        filters += [{'Name':'tag:imh:version', 'Values':['{0}-*'.format(version)]}]
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
    previousCreationDate = 0
    mostRecent = {}
    for key, value in targetAmi.iteritems():
        if key == 'Images':
            for item in value:
                if item['CreationDate'] > previousCreationDate:
                    previousCreationDate = item['CreationDate']
                    mostRecent['Name'] = ''
                    mostRecent['Value'] = item['ImageId']
                    for i in item['Tags']:
                        if i['Key'] == 'imh:version':
                            mostRecent['Name'] = i['Value']
    return mostRecent

userPrefix = 'development'
ami = getAmiForVersionRole('hybris', userPrefix)
print(extractData(ami))
