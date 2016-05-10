#!/usr/bin/python

import boto3


def extractLoadBalanceData(elb, loadBalancer):
    extractedData = elb.describe_load_balancers(LoadBalancerNames=[loadBalancer])
    return extractedData


def extractTagData(elb, loadBalancer):
    extractedData = elb.describe_tags(LoadBalancerNames=[loadBalancer])
    return extractedData


def lambda_handler(event, context):
    elb = boto3.client('elb')
    loadBalanceData = extractLoadBalanceData(elb, event['loadBalancer'])
    tagData = extractTagData(elb, event['loadBalancer'])
    mergedData = dict(); mergedData.update(tagData)
    return mergedData
