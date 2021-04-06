  def get_user(self,user_uid):
    resource = self.endpoint + "/admin/user"
    parameters = {'uid': user_uid}
    timestamp = formatdate(usegmt=True)
    string_to_sign = 'GET\n\n\n' + timestamp + "\n" + "/admin/user"
    signature = base64.encodestring(hmac.new(self.secret_key.encode('UTF-8'),string_to_sign.encode('UTF-8'),sha1).digest()).strip().decode()
    authorization = 'AWS ' + self.access_key + ":" + signature
    return json.dumps({'Date': timestamp, 'Authorization' : authorization })
