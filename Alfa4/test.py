import sys, time,json
from socket import *

s = socket(AF_INET, SOCK_DGRAM)
s.bind(('', 9876))
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

while 1:
    query = {"command": "hello", "peer_id": "yo"}
    query_json = json.dumps(query).encode()
    s.sendto(query_json, ('<broadcast>', 9876))
    time.sleep(2)