import httplib, urllib
conn = httplib.HTTPConnection("127.0.0.1:5000")
headers = {"Content-type": "application/json"}
while True:
    conn.request("POST", "/metric/api/v1.0/message", '{"Origin":"10.0.0.9", "Message": "Hallo Welt :D", "Type": "1"}', headers)
    print conn.getresponse()