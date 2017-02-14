# aviatrix-gateway-rest-api
Creating Aviatrix gateway via REST API

aviatrix.py will load default configurations from aviatrix.cfg.
On running aviatrix.py, it will follow these steps:
* Create new session with username
* Associate Aviatrix license with CID.
* Set max number of VPCs.
* Create a user account and associate it with AWS account.
* Create a VPC in AWS and launch gateway.

### Sample output

Creating new session with username....

https://192.168.0.3/v1/api?action=login&username=admin&password=av1@Tr1x

Created new session with CID 58a3762955546


Getting license info....

https://192.168.0.3/v1/api?CID=58a3762955546&action=setup_customer_id&customer_id=prashant-1487057566.92

License associalted with prashant-1487057566.92


Setting maximum VPCs....

https://192.168.0.3/v1/api?CID=58a3762955546&action=setup_max_vpc_containers&vpc_num=2

Setting maximum number of VPSs as 2.

Available CIDRs 192.168.0.64/26, 192.168.0.128/26, 192.168.0.192/26


Creating User account and associating with AWS....

{u'return': True, u'results': u'An email with instructions has been sent to rakeshranjan.568@gmail.com'}

Account creation successful. An email with instructions has been sent to rakeshranjan.568@gmail.com


Creating VPC with CIDR 192.168.0.64/26

{u'return': True, u'results': u'VPC is successfully created. An email with instructions has been sent to rakeshranjan.568@gmail.com'}

VPC Creation Successful VPC is successfully created. An email with instructions has been sent to rakeshranjan.568@gmail.com

