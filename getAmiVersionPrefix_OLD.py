#!/usr/bin/python
# VERSION NOT ALWAYS GIVEN !!!!!!
import boto3, re


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

def extractData(targetAmi, versionPrefix):
    #Name = role, Value = versionPrefix
    #TODO: Get version from targetAmi
    currentTimestamp = 0
    role = ''
    version =''
    mostRecent = {}
    mostRecentList = []
    versionRegEx = '^{0}.*'.format(versionPrefix)
    for key, value in targetAmi.iteritems():
        if key == 'Images':
            for item in value:
                if item['CreationDate'] > currentTimestamp:
                    currentTimestamp = item['CreationDate']
                    for i in item['Tags']:
                        if i['Key'] == 'imh:version':
                            versionMatch = re.match(versionRegEx, i['Value'])
                            if versionMatch:
                                version = i['Value']
                        if i ['Key'] == 'imh:role':
                            role = i['Value']
                    mostRecent['Role'] = role
                    mostRecent['versionPrefix'] = version
                    mostRecentList.append(mostRecent)
                    #loop through and check version starts with development
    return mostRecentList

userVersion = 'development'
#amiVersion = getAmiForVersionRole('hybris', 'feature-WSP-786-4')
ami = getAmiForVersionRole('hybris', userVersion)
print(extractData(ami, userPrefix))
#version = extractVersion(amiVersion)
#print('List Version: {0} \n\n'.format(extractData(amiVersion, version)))
