import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import json
import re

from search import search

all_ings = []
f = open('all_ings.txt')
for row in f.readlines():
    ing = row.strip()
    all_ings.append({'value': ing})
f.close()
# all_ings = all_ings[: 10]

def get_suggestions(query):
    final_ings = []
    qp = query.strip().split(',')
    final_query = re.sub('[^A-Za-z0-9 ]+', '', qp[-1])
    final_query = final_query.strip()
    print (final_query)
    for ing in all_ings:
        if ing['value'].find(final_query) == 0:
            final_ings.append(ing)
    final_ings.sort(key=lambda x: x['value'])
    if len(final_ings) > 5:
        final_ings = final_ings[: 5]
    return final_ings

HOST_NAME = 'localhost' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 12345 # Maybe set this to 9000.

class MyHandler(BaseHTTPRequestHandler):
    # def do_HEAD(s):
    #     s.send_response(200)
    #     s.send_header("Content-type", "text/html")
    #     s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        print (s.path)
        getParams = parse_qs(urlparse(s.path).query)
        print (getParams)
        ans = None
        query = getParams
        query_str = getParams['text'][0]
        request = getParams['request'][0]
        if request == '1':
            ans = get_suggestions(query_str)
            print (ans[0])
            print (json.dumps(ans[0]))
        else:
            ans = search(query)
        s.send_response(200)
        s.send_header("Content-type", "application/json")
        s.send_header("Access-Control-Allow-Origin", "*")
        s.end_headers()
        s.wfile.write(bytes(json.dumps(ans), 'utf-8'))

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print (time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print (time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))
