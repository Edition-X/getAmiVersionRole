#!/usr/bin/python
# VERSION NOT ALWAYS GIVEN !!!!!!
import boto3


def getAmiForVersionRole(version, role):
    ec2client = boto3.client('ec2')
    filters = [{'Name':'tag:imh:role', 'Values':[role]}]
    if version:
        filters += [{'Name':'tag:imh:version', 'Values':[version]}]
    targetAmi = ec2client.describe_images(
           Filters = filters
    )
    return targetAmi

def extractData(version, targetAmi):
    #Name = version, Value = AMI_ID
    versionToImageId = {}
    versionList = []
    for key, value in targetAmi.iteritems():
        if key == 'Images': 
            for item in value:
                versionToImageId['Name'] = version
                versionToImageId['Value'] = item['ImageId']
                versionList.append(versionToImageId)
    return versionList


ami = getAmiForVersionRole('8.10.0-release-1', 'hybris')
extractData('8.10.0-release-1', ami)
