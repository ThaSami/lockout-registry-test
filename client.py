import requests
import argparse
import sys

def islocked(url,service):
    data = {"service": service}
    response = requests.post(url, json=data)
    return response.text.lower() == "locked"


def read_config():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="url to connect to")
    parser.add_argument("--servicename", help="service name to check for")
    args = parser.parse_args()
    return args



if __name__=="__main__":
    args = read_config()
    url = args.url
    service = args.servicename
    if islocked(url,service):
        print("Service Is Locked")
        sys.exit(1)
