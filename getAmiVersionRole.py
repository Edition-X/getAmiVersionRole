#!/usr/bin/python
# VERSION NOT ALWAYS GIVEN !!!!!!
import boto3


def getAmiForVersionRole(role, version = None):
    ec2client = boto3.client('ec2')
    filters = [{'Name':'tag:imh:role', 'Values':[role]}]
    if version:
        filters += [{'Name':'tag:imh:version', 'Values':[version]}]
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

def extractData(targetAmi, version):
    #Name = version, Value = AMI_ID
    #TODO: Get version from targetAmi
    versionToImageId = {}
    versionList = []
    for key, value in targetAmi.iteritems():
        if key == 'Images':
            for item in value:
                versionToImageId['Name'] = version
                versionToImageId['Value'] = item['ImageId']
                versionList.append(versionToImageId)
    return versionList

userVersion = '8.10.0-release-1'
amiVersion = getAmiForVersionRole('hybris', userVersion)
version = extractVersion(amiVersion)
print('List Version: {0} \n\n'.format(extractData(amiVersion, version)))
