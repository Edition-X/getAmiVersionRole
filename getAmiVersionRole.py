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

def extractToDict(version, targetAmi):
    #Name = version, Value = AMI_ID
    versionToImageId = {}
    versionList = []
    for key, value in targetAmi.iteritems():
        if key == 'Images': 
            for item in value:
                versionToImageId['Name'] = vers
                amiDict[('Name','Value')] = [[version],[item['ImageId']]
    return amiDict
               # for key2, value2 in x.iteritems():
               #     if key2 == 'ImageId':
               #         amiDict[('Name','Value')] = [[version], [value2]]
               #         import pdb; pdb.set_trace() 

#if key == "ImageId":
            #print(key, value)
#import pdb; pdb.set_trace()

#print("Without version:\n")
#print(getAmiForVersion('', 'hybris'))
#print("\n_________________________________\n")
#print("With version:\n")
ami = getAmiForVersion('8.10.0-release-1', 'hybris')
extractToDict('8.10.0-release-1', ami)
