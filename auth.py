#!/bin/python3

import argparse
import base64
import hmac
import json
import requests

from datetime import datetime
from email.utils import formatdate
from hashlib import sha1
from urllib import parse as urlparse

class CephClient:
  def __init__(self,accesskey,secretkey):
    self.access_key = accesskey
    self.secret_key = secretkey

  def get_headers(self,http_method,api_endpoint,body=False):
    timestamp = formatdate(usegmt=True)
    if body == False:
       string_to_sign = http_method + "\n\n\n" + timestamp + "\n" + api_endpoint
    else:
       content_type = "application/json"
       string_to_sign = http_method + "\n\n" + content_type + "\n" + timestamp + "\n" + api_endpoint
    signature = base64.encodestring(hmac.new(self.secret_key.encode('UTF-8'),string_to_sign.encode('UTF-8'),sha1).digest()).strip().decode()
    authorization = 'AWS ' + self.access_key + ":" + signature
    return json.dumps({'Date': timestamp, 'Authorization' : authorization })

parser = argparse.ArgumentParser(description='Returns both Date and Authorization headers')
parser.add_argument('accesskey',help='The access key of the administrative user')
parser.add_argument('secretkey',help='The secret key of the administrative user')
parser.add_argument('operation',help='The operation to be performed. Valid operations are: \n get_user \n create_user \n mod_user \n add_cap \n add_key \n remove_cap \n remove_key \n remove_user')
parser.add_argument('--bucket',help='The bucket name to create or retrieve')
parser.add_argument('--object',help='The object name to create or retrieve')
args = parser.parse_args()

s3 = CephClient(args.accesskey,args.secretkey)

if args.operation == "get_user" or args.operation == "get_user_quota" or args.operation == "get_bucket_quota": print(s3.get_headers("GET","/admin/user"))
if args.operation == "create_user" or args.operation == "add_cap" or args.operation == "add_key": print(s3.get_headers("PUT","/admin/user"))
if args.operation == "mod_user": print(s3.get_headers("POST","/admin/user"))
if args.operation == "remove_cap" or args.operation == "remove_key" or args.operation == "remove_user": print(s3.get_headers("DELETE","/admin/user"))
   
if args.operation == "get_bucket_info" or args.operation == "get_bucket_index": print(s3.get_headers("GET","/admin/bucket"))
if args.operation == "get_bucket_policy": print(s3.get_headers("GET","/admin/bucket?policy"))
if args.operation == "link_bucket": print(s3.get_headers("PUT","/admin/bucket"))
if args.operation == "unlink_bucket": print(s3.get_headers("POST","/admin/bucket"))
if args.operation == "remove_object" or args.operation == "remove_bucket": print(s3.get_headers("DELETE","/admin/bucket"))

if args.operation == "put_bucket": print(s3.get_headers("PUT","/" + args.bucket))
if args.operation == "get_bucket": print(s3.get_headers("GET","/" + args.bucket))

if args.operation == "put_object": print(s3.get_headers("PUT","/" + args.bucket + "/" + args.object))
if args.operation == "get_object": print(s3.get_headers("GET","/" + args.bucket + "/" + args.object))

if args.operation == "set_user_quota" or args.operation == "set_bucket_quota": print(s3.get_headers("PUT","/admin/user",True))
if args.operation == "set_individual_bucket_quota": print(s3.get_headers("PUT","/admin/bucket",True))

if args.operation == "get_usage": print(s3.get_headers("GET","/admin/usage"))
if args.operation == "remove_usage": print(s3.get_headers("DELETE","/admin/usage"))
