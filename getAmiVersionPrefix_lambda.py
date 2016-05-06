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
    if targetAmi and len(targetAmi['Images']) and not role:
        return Exception('No AMI found for version: {0}'.format(version))
    return targetAmi


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


def lambda_handler(event, context):
    ami = getAmiForVersionRole(event['role'], event['versionPrefix'])
    return extractData(ami)

#userPrefix = 'development'
#ami = getAmiForVersionRole('hybris', userPrefix)
#print(extractData(ami))
