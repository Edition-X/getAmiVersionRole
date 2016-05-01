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

def extractData(targetAmi, version = '8.10.0-release-1'):
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

version = '8.10.0-release-1'
amiNoVersion = getAmiForVersionRole('hybris')
amiVersion = getAmiForVersionRole('hybris', version)

#print('AMI No Version: {0} \n\n'.format(amiNoVersion))
#print('AMI Version: {0} \n\n'.format(amiVersion))
print('List No Version: {0} \n\n'.format(extractData(amiNoVersion)))
print('List Version: {0} \n\n'.format(extractData(amiVersion, version)))
