#!python
# This is a RESTFUL client to perform administrative tasks on a Ceph cluster

import base64
import hmac
import requests

from datetime import datetime
from email.utils import formatdate
from hashlib import sha1
from urllib import parse as urlparse

class CephClient:
  def __init__(self,accesskey,secretkey,endpoint_url):
    self.access_key = accesskey
    self.secret_key = secretkey
    self.endpoint = endpoint_url

  def get_user(self,user_uid):
    resource = self.endpoint + "/admin/user"
    parameters = {'uid': user_uid}
    timestamp = formatdate(usegmt=True)
    string_to_sign = 'GET\n\n\n' + timestamp + "\n" + "/admin/user"
    signature = base64.encodestring(hmac.new(self.secret_key.encode('UTF-8'),string_to_sign.encode('UTF-8'),sha1).digest()).strip().decode()
    authorization = 'AWS ' + self.access_key + ":" + signature
    r = requests.get(resource,headers={'Date':timestamp,'Authorization':authorization},params=parameters)
    print(r.text)

  def create_user(self,uid,display_name):
    resource = self.endpoint + "/admin/user"
    parameters = {'uid': uid,'display-name':display_name}
    timestamp = formatdate(usegmt=True)
    string_to_sign = 'PUT\n\n\n' + timestamp + "\n" + "/admin/user"
    signature = base64.encodestring(hmac.new(self.secret_key.encode('UTF-8'),string_to_sign.encode('UTF-8'),sha1).digest()).strip().decode()
    authorization = 'AWS ' + self.access_key + ":" + signature
    r = requests.put(resource,headers={'Date':timestamp,'Authorization':authorization},params=parameters)
    print(r.text)
    
  def remove_user(self,uid):
    resource = self.endpoint + "/admin/user"
    parameters = {'uid': uid}
    timestamp = formatdate(usegmt=True)
    string_to_sign = 'DELETE\n\n\n' + timestamp + "\n" + "/admin/user"
    signature = base64.encodestring(hmac.new(self.secret_key.encode('UTF-8'),string_to_sign.encode('UTF-8'),sha1).digest()).strip().decode()
    authorization = 'AWS ' + self.access_key + ":" + signature
    r = requests.delete(resource,headers={'Date':timestamp,'Authorization':authorization},params=parameters)
    print(r.status_code)

  def get_bucket_quota(self,uid):
    resource = self.endpoint + "/admin/user"
    parameters = {'quota':'','uid': uid,'quota-type':'bucket'}
    timestamp = formatdate(usegmt=True)
    string_to_sign = 'GET\n\n\n' + timestamp + "\n" + "/admin/user"
    signature = base64.encodestring(hmac.new(self.secret_key.encode('UTF-8'),string_to_sign.encode('UTF-8'),sha1).digest()).strip().decode()
    authorization = 'AWS ' + self.access_key + ":" + signature
    r = requests.get(resource,headers={'Date':timestamp,'Authorization':authorization},params=parameters)
    print(r.text)

  def set_bucket_quota(self,uid):
    resource = self.endpoint + "/admin/user"
    parameters = {'quota':'','uid': uid,'quota-type':'bucket'}
    payload = json.dumps({"enabled": 'true',"check_on_raw": 'true',"max_size":1099511627776,"max_size_kb":1073741824,"max_objects":-1})
    timestamp = formatdate(usegmt=True)
    string_to_sign = 'PUT\n\n\n' + timestamp + "\n" + "/admin/user"
    signature = base64.encodestring(hmac.new(self.secret_key.encode('UTF-8'),string_to_sign.encode('UTF-8'),sha1).digest()).strip().decode()
    authorization = 'AWS ' + self.access_key + ":" + signature
    r = requests.put(resource,headers={'Date':timestamp,'Authorization':authorization},params=parameters,data=payload)
    print(r.status_code)

  def set_individual_bucket_quota(self,uid,bucket,quota_settings):
    resource = self.endpoint + "/admin/bucket"
    parameters = {'quota':'','uid': uid,'bucket':bucket}
    payload = json.dumps(quota_settings)
    timestamp = formatdate(usegmt=True)
    string_to_sign = 'PUT\n\n\n' + timestamp + "\n" + "/admin/bucket"
    signature = base64.encodestring(hmac.new(self.secret_key.encode('UTF-8'),string_to_sign.encode('UTF-8'),sha1).digest()).strip().decode()
    authorization = 'AWS ' + self.access_key + ":" + signature
    r = requests.put(resource,headers={'Date':timestamp,'Authorization':authorization},params=parameters,data=payload)
    print(r.status_code)
