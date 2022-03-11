import pulumi,ipaddress
import pulumi_aws as aws 
from pulumi_aws import get_availability_zones
from nat import Create_nat



#function to create vpc and dependencies, cidr block defaulted as well as az
def Createvpc(name, az = 2, cidr_block='10.0.0.0/16'):
    
    subnet = list(ipaddress.ip_network(cidr_block).subnets(new_prefix=24))
    
    #obtain available az
    available = aws.get_availability_zones(state="available").names[:(az*2)]
    
    #create VPC 
    vpc = aws.ec2.Vpc(f"{name}-vpc",                    cidr_block=cidr_block,
    enable_dns_hostnames= True,
    tags= {
        "Name": f"{name}"
    })
    
    pulumi.export("vpc arn", vpc.arn)
    pulumi.export("id", vpc.id)
    
    #internet gateway
    igw = aws.ec2.InternetGateway(f'{name}-igw',
                              vpc_id=vpc.id,
                              tags={'Name': f'{name}-IGW'}
                              )
    
    #nat gateway
    Create_nat(name= name,subnet_id=publicID)
    
    #ID for subnets
    privateID = []
    publicID = []
    
    #create subnets
    for n in range(az):
        #publci subnet 
        public_subnet = aws.ec2.Subnet(f"{name}-public-{n}",
            vpc_id = vpc.id,
            availability_zone= available[n],
            cidr_block= str(subnet[n]),
            map_public_ip_on_launch= True,
            tags={
                "Name": f"Public Subnet-{name}-{n}",
                "AZ": f"{available[n]}"
            }
            )
        #private subnet
        private_subnet = aws.ec2.Subnet(f"{name}-private-{n}",
            vpc_id = vpc.id,
            availability_zone= available[n],
            cidr_block= str(subnet[n+len(available)]),
            tags={
                "Name": f"Private Subnet-{name}-{n}",
                "AZ": f"{available[n]}"
            }
            )
        publicID.append(public_subnet.id)
        privateID.append(private_subnet.id)
    
    
    # route table for private subnets NOT DONE
    rt_private = aws.ec2.RouteTable(f"{name}",
                               vpc_id = vpc.id,
                               route=[
                                   aws.ec2.RouteTableRouteArgs(
                                       cidr_block= "0.0.0.0/0",
                                       gateway_id= ""
                                   )
                               ],
                               tags = {
                                   "Name": f"{name}-private-rt"
                               })
    rt_public = aws.ec2.RouteTable(f"{name}",
                               vpc_id = vpc.id,
                               route=[
                                   aws.ec2.RouteTableRouteArgs(
                                       cidr_block= "0.0.0.0/0",
                                       gateway_id= igw.id
                                   )
                               ],
                               tags = {
                                   "Name": f"{name}-public-rt"
                               })
    
        
    
    
