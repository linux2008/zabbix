#!/usr/bin/python

import requests
import json
import sys

def connRequest(data):
    url='http://192.168.133.129/zabbix/api_jsonrpc.php'
    headers={'Content-Type': 'application/json-rpc'}
    request=requests.post(url=url,headers=headers,data=json.dumps(data))
    req=request.content
    return json.loads(req)

def authorize():
    data={
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": "Admin",
            "password": "zabbix"
        },
        "id": 1,
        "auth": None
    }
    req=connRequest(data)
    if not 'result' in req:
        print 'login failed'
    else:
        return req['result']

def getGroupID(auth):
    data1={
        "jsonrpc": "2.0",
        "method": "hostgroup.get",
        "params": {
            "output": "extend",
            "filter": {
                "name": [
                    "Linux servers"
                ]
             }
        },
        "auth":auth,
        "id": 2
        }  
    req1=connRequest(data1)
    return req1['result'][0]['groupid']

def getTemplate(auth):
    data2={
    "jsonrpc": "2.0",
    "method": "template.get",
    "params": {
        "output": "templateids",
        "filter": {
            "host": [
                "Template OS Linux",
            ]
        }
    },
    "auth": auth,
    "id": 3
    }
    req2=connRequest(data2)
    return req2['result'][0]['templateid']

def hostExists(auth,hostname):
    data3={
    "jsonrpc": "2.0",
    "method": "host.exists",
    "params": {
        "host": hostname
    },
    "auth": auth,
    "id": 4
    }
    req3=connRequest(data3)
    return req3['result']

def addHost(auth,hostname,ip):
    data4={
    "jsonrpc": "2.0",
    "method": "host.create",
    "params": {
        "host": hostname,
        "interfaces": [
            {
                "type": 1,
                "main": 1,
                "useip": 1,
                "ip": ip,
                "dns": "",
                "port": "10050"
            }
        ],
        "groups": [
            {
                "groupid": getGroupID(auth)
            }
        ],
        "templates": [
            {
                "templateid": getTemplate(auth)
            }
        ],
    },
    "auth": auth,
    "id":5
    }
    if hostExists(auth,hostname):
        print '%s is exists' %hostname
        sys.exit(1)
    else: 
        req4=connRequest(data4)
        return req4



if __name__=='__main__':
    auth=authorize()
    hostname='agent01'
    ip='192.168.133.128'
    print addHost(auth,hostname,ip)
