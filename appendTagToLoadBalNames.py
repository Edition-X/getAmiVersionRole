#!/usr/bin/python

import boto3


def extractLoadBalanceData(elb, loadBalancer):
    extractedData = elb.describe_load_balancers(LoadBalancerName=[loadBalancer])
    return extractedData


def extractTagData(elb, loadBalancer):
    extractedData = elb.describe_tags(LoadBalancerNames=[loadBalancer])
    return extractedData


loadBalancer = 'imh-acceptance-web'
elb = boto3.client('elb')
