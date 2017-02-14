import requests
import sys
import os
import requests
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def readCfgFile(cfgFileName):

    global BASE_URL
    global ADMIN_USER
    global ADMIN_PASS
    global CID
    global LICENSE_TOKEN
    global USER_ACCOUNT_NAME
    global USER_ACCOUNT_PASSWORD
    global USER_ACCOUNT_EMAIL
    global CLOUD_TYPE
    global AWS_ACCOUNT_NUMBER
    global AWS_ACCESS_KEY
    global AWS_SECRET_KEY
    global VPC_NAME
    global VPC_REGION
    global GW_SIZE
    
    file = open(cfgFileName, "r")
    for newLine in file:
        strlen = len(newLine)
        newLine = newLine[:strlen - 1]
        equalIndex = newLine.find("=")
        key = newLine[:equalIndex]
        value = newLine[equalIndex+1:].strip()

        if(key == 'base_url'):
            BASE_URL = value
        if(key == 'admin_user'):
            ADMIN_USER = value
        if(key == 'admin_pass'):
            ADMIN_PASS = value
        if(key == 'cid'):
            CID = value
        if(key == 'license_token'):
            LICENSE_TOKEN = value
        if(key == 'user_account_name'):
            USER_ACCOUNT_NAME = value
        if(key == 'user_account_password'):
            USER_ACCOUNT_PASSWORD = value
        if(key == 'user_account_email'):
            USER_ACCOUNT_EMAIL = value
        if(key == 'cloud_type'):
            CLOUD_TYPE = value
        if(key == 'aws_account_number'):
            AWS_ACCOUNT_NUMBER = value
        if(key == 'aws_access_key'):
            AWS_ACCESS_KEY = value
        if(key == 'aws_secret_key'):
            AWS_SECRET_KEY = value
        if(key == 'vpc_name'):
            VPC_NAME = value
        if(key == 'vpc_region'):
            VPC_REGION = value
        if(key == 'gw_size'):
            GW_SIZE = value

        
def createSession():
    def createSessionSuccessCb(response_json):
        #print response_json
        global CID
        CID = response_json['CID']
        print "Created new session with CID %s\n" %CID
    args = 'action=login&username=' + ADMIN_USER + '&password=' + ADMIN_PASS
    print "Creating new session with username.... "
    do_get(args, createSessionSuccessCb)

def getLicenseInfo():
    def getLicenseInfoSuccessCb(response_json):
        print "License associalted with %s\n" %response_json['results']['CustomerID'] 
    args = 'CID='+CID+'&action=setup_customer_id&customer_id=' + LICENSE_TOKEN 
    print "Getting license info.... "
    do_get(args, getLicenseInfoSuccessCb)

def setMAxVpcCont():
    max_vpc_num = 2
    def setMaxVpcContSuccessCb(response_json):
        global CIDR_LIST
        CIDR_LIST = response_json['results']['cidr_list']
        print "Setting maximum number of VPSs as %d. \nAvailable CIDRs %s\n" %(max_vpc_num, ', '.join(CIDR_LIST))
    args = 'CID='+CID+'&action=setup_max_vpc_containers&vpc_num=' + str(max_vpc_num)
    print "Setting maximum VPCs.... "
    do_get(args, setMaxVpcContSuccessCb)

def createUserAccount():
    def createUserAccountSuccessCb(response_json):
        print "Account creation successful. %s\n" %response_json['results']

    data = {"CID": CID, "action": "setup_account_profile", "account_name": USER_ACCOUNT_NAME, "account_password": USER_ACCOUNT_PASSWORD, "account_email": USER_ACCOUNT_EMAIL, "cloud_type": CLOUD_TYPE, "aws_account_number": AWS_ACCOUNT_NUMBER, "aws_access_key": AWS_ACCESS_KEY, "aws_secret_key": AWS_SECRET_KEY}
    print "Creating User account and associating with AWS.... "
    do_post(data, createUserAccountSuccessCb)

def createVpcDatacenter():
    def createVpcDatacenterSuccessCb(response_json):
        print "VPC Creation Successful %s" %response_json['results']

    data = {"CID": CID, "action": "create_container", "cloud_type": CLOUD_TYPE, "account_name": USER_ACCOUNT_NAME, "vpc_name": VPC_NAME, "vpc_reg": VPC_REGION, "vpc_size": GW_SIZE, "vpc_net": CIDR_LIST[0]}
    print "Creating VPC with CIDR %s" %CIDR_LIST[0]
    do_post(data, createVpcDatacenterSuccessCb)

def do_get(args, callback):
    url = BASE_URL+'?'+args
    print url
    response = requests.get(url, verify=False)
    #print response.status_code
    response_json = response.json()
    #print response_json
    if response_json['return'] == True:
        return callback(response_json)
    else:
        print "Failed: %d error - %s" %(response.status_code, str(response_json['reason']))
        exit

def do_post(data, callback):
    response = requests.post(BASE_URL, data=data, verify=False)
    response_json = response.json()
    print response_json
    if response_json['return'] == True:
        return callback(response_json)
    else:
        print "Failed: %d error - %s" %(response.status_code, str(response_json['reason']))
        exit

readCfgFile('aviatrix.cfg')
createSession()
getLicenseInfo()
setMAxVpcCont()
createUserAccount()
createVpcDatacenter()

