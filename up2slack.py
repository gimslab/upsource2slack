import time, BaseHTTPServer
import httplib, urllib
import json
 
HOST_NAME = 'my.server.com'
PORT_NUMBER = 18081
 
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
 
class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_POST(s):
    s.data_string = s.rfile.read(int(s.headers['Content-Length']))
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    print s.data_string
    j = json.loads(s.data_string)
    msg = j["dataType"] + " <http://upsource.server.com/>"
    print msg
    params = urllib.urlencode({'payload' : '{"text":"'+msg+'"}'})
    conn = httplib.HTTPConnection("1.1.1.1", 8888) # proxy setting
    conn.request("POST", "https://hooks.slack.com/services/xxxxxx", params, headers)
    response = conn.getresponse()
    print "sent to slack"
    conn.close

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
