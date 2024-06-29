import base64
import json
import pprint
import sys

session_key = 'uh7814kdqobk5pa57shpdc4mrmocd1rx|.eJxVjEEOwiAQAP_C2RBYQIpH776BsCwrVUOT0p6MfzckPeh1ZjJvEdO-1bj3ssaZxEU4cfplmPKztCHokdp9kXlp2zqjHIk8bJe3hcrrerR_g5p6HVv02npjDRskBB0QwqSsQaaS2YeiOZ2B\
FbqQgRlJGT2xywXYowclPl_rUzhj:1sLu8M:ijwLgZeez2gkqezNvyHDwsouPGsu1i-FnfmNsYhf4bk'

def get_session_dictionary(session_key):

    binary_key, payload = base64.b64decode(session_key).split(b':', 1)
    session_dictionary = json.loads(payload.decode())

    return session_dictionary

if __name__ == '__main__':
    if len(sys.argv)>1:
        session_key = sys.argv[1]
        session_dictionary = get_session_dictionary(session_key)
        pp = pprint.PrettyPrinter(indent=4)
        pp.print(session_dictionary)
