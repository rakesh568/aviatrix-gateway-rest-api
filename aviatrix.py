import requests
import sys
import os
import requests
import time
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class aviatrixController:
    def __init__(self, cfg):
        self.cfg=cfg
        self.cidr_list = []
        line_regex = "([a-zA-Z_]+)=(.+)"
        try:
            file = open(self.cfg, "r")
        except IOError as e:
            print "Cannot open", self.cfg
            raise
        for line in file:
            match = re.match(line_regex, line)
            if match:
                setattr(self, match.group(1), match.group(2))


    def createSession(self):
        def createSessionSuccessCb(response_json):
            try:
                self.cid = response_json['CID']
                print "Created new session with CID %s\n" %self.cid
            except KeyError, e:
                print "Unable to create session. %s" %str(e)
                raise

        args = 'action=login&username=' + self.admin_user + '&password=' + self.admin_pass
        print "Creating new session with username.... "
        self.do_get(args, createSessionSuccessCb)


    def getLicenseInfo(self):
        def getLicenseInfoSuccessCb(response_json):
            try:
                print "License associated with %s\n" %response_json['results']['CustomerID']
            except KeyError, e:
                print "Unable to get license info for customer ID: %s.\n%s" %(self.license_token, str(e))
                raise
        args = 'CID='+self.cid+'&action=setup_customer_id&customer_id=' + self.license_token
        print "Getting license info.... "
        self.do_get(args, getLicenseInfoSuccessCb)

    def setMAxVpcCont(self):
        max_vpc_num = 2
        def setMaxVpcContSuccessCb(response_json):
            try:
                self.cidr_list = response_json['results']['cidr_list']
                print "Setting maximum number of VPSs as %d. \nAvailable CIDRs %s\n" %(max_vpc_num, ', '.join(self.cidr_list))
            except KeyError, e:
                print "Unable to set VPC containers. %s" %str(e)
                raise

        args = 'CID='+self.cid+'&action=setup_max_vpc_containers&vpc_num=' + str(max_vpc_num)
        print "Setting maximum VPCs.... "
        self.do_get(args, setMaxVpcContSuccessCb)
        
    def createUserAccount(self):
        def createUserAccountSuccessCb(response_json):
            try:
                print "Account creation successful. %s\n" %response_json['results']
            except KeyError, e:
                print "Unable to create User account. %s" %str(e)
                raise

        data = {"CID": self.cid, "action": "setup_account_profile", "account_name": self.user_account_name, "account_password": self.user_account_password, "account_email": self.user_account_email, "cloud_type": self.cloud_type, "aws_account_number": self.aws_account_number, "aws_access_key": self.aws_access_key, "aws_secret_key": self.aws_secret_key}
        print "Creating User account and associating with AWS.... "
        self.do_post(data, createUserAccountSuccessCb)


    def createVpcDatacenter(self):
        def createVpcDatacenterSuccessCb(response_json):
            try:
                print "VPC/gateway Creation Successful %s" %response_json['results']
            except KeyError, e:
                print "Unable to create VPC/gateway."
                raise

        data = {"CID": self.cid, "action": "create_container", "cloud_type": self.cloud_type, "account_name": self.user_account_name, "vpc_name": self.vpc_name, "vpc_reg": self.vpc_region, "vpc_size": self.gw_size, "vpc_net": self.cidr_list[0]}
        print "Creating VPC with CIDR %s" %self.cidr_list[0]
        self.do_post(data, createVpcDatacenterSuccessCb)


    def do_get(self, args, callback):
        url = self.base_url+'?'+args
        print url
        try:
            response = requests.get(url, verify=False)
        except Exception, e:
            print "Unable to establish connection."
            raise
        
        response_json = response.json()
        if response_json['return'] == True:
            return callback(response_json)
        else:
            print "Failed: %d error - %s" %(response.status_code, str(response_json['reason']))
            raise Exception("Get request error.")

    def do_post(self, data, callback):
        try:
            response = requests.post(self.base_url, data=data, verify=False)
        except Exception, e:
            print "Unable to establish connection."
            raise
        
        response_json = response.json()
        if response_json['return'] == True:
            return callback(response_json)
        else:
            print "Failed: %d error - %s" %(response.status_code, str(response_json['reason']))
            raise Exception("Post request error.")
        
myController = aviatrixController("aviatrix.cfg")
myController.createSession()
myController.getLicenseInfo()
myController.setMAxVpcCont()
myController.createUserAccount()
myController.createVpcDatacenter()

