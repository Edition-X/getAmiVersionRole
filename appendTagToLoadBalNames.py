#!/usr/bin/python

import boto3

elb = boto3.client('elb')
#print(elb.describe_load_balancers())
print(elb.describe_tags(LoadBalancerNames=['imh-test3-web']))

#def extractLoadBalanceData(elb, loadBalancer):
#    extractedData = elb.describe_load_balancers(LoadBalancerNames=[loadBalancer])
#    return extractedData
#
#
#def extractTagData(elb, loadBalancer):
#    extractedData = elb.describe_tags(LoadBalancerNames=[loadBalancer])
#    return extractedData
#
#loadBalancer = 'imh-test4-web'
#elb = boto3.client('elb')
#loadBalanceData = extractLoadBalanceData(elb, loadBalancer)
#tagData = extractTagData(elb, loadBalancer)
##z = loadBalanceData.copy()
##z = z.update(tagData)
#z = dict(loadBalanceData)
#z.update(tagData)
#
#
##print('LBD: {0}'.format(loadBalanceData))
#print(extractLoadBalanceData(elb, 'imh-acceptance-web'))
##print('Tag: {0}'.format(tagData))
##print('And the winner is... \n\n\n\n')
##print(z)
