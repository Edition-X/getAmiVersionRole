#!/usr/bin/python
import boto3
import json
import datetime
from time import mktime

class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(mktime(obj.timetuple()))

    return json.JSONEncoder.default(self, obj)

def lambda_handler(event, context):
    elb = boto3.client('elb')
    return json.dumps(elb.describe_load_balancers(event[loadBalancer]), cls = MyEncoder)
