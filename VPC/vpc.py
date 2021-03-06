import pulumi,ipaddress
import pulumi_aws as aws 
from pulumi_aws import get_availability_zones
from VPC.sg import Create_sg
from VPC.nat import Create_nat




#function to create vpc and dependencies, cidr block defaulted as well as az
def Createvpc(name, az = 1, cidr_block='10.0.0.0/16'):
    
    subnet = list(ipaddress.ip_network(cidr_block).subnets(new_prefix=24))
    
    #obtain available az
    available = aws.get_availability_zones(state="available").names[:(az*2)]
    
    #create VPC 
    vpc = aws.ec2.Vpc(f"{name}-vpc",
    cidr_block=cidr_block,
    enable_dns_hostnames= True,
    tags= {
        "Name": f"{name}"
    })
    
    
    
    #internet gateway
    igw = aws.ec2.InternetGateway(f'{name}-igw',
                              vpc_id=vpc.id,
                              tags={'Name': f'{name}-IGW'}
                              )
    
    
    #ID for subnets
    privateID = []
    publicID = []
    
    #create subnets
    for n in range(az):
        #public subnet 
        public_subnet = aws.ec2.Subnet(f"{name}-public-{n}",
            vpc_id = vpc.id,
            availability_zone= available[n],
            cidr_block= str(subnet[n]),
            map_public_ip_on_launch= True,
            tags={
                "Name": f"{name}-Public-Subnet-{n}",
                "AZ": f"{available[n]}"
            }
            )
        #private subnet
        private_subnet = aws.ec2.Subnet(f"{name}-private-{n}",
            vpc_id = vpc.id,
            availability_zone= available[n],
            cidr_block= str(subnet[n+len(available)]),
            tags={
                "Name": f"{name}-Private-Subnet-{n}",
                "AZ": f"{available[n]}"
            }
            )
        publicID.append(public_subnet.id)
        privateID.append(private_subnet.id)
    
    #nat gateway
    nat = Create_nat(name= name,subnet_id=publicID)
    #security group
    sg = Create_sg(vpc_id=vpc.id,name=name)
    session= ["com.amazonaws.us-east-1.ssm","com.amazonaws.us-east-1.ssmmessages","com.amazonaws.us-east-1.ec2messages"]
    
    for num in range(az):     
        rt_private = aws.ec2.RouteTable(f"{name}-private-subnet-rt",
                               vpc_id = vpc.id,
                               routes=[
                                   aws.ec2.RouteTableRouteArgs(
                                       cidr_block= "0.0.0.0/0",
                                       nat_gateway_id= nat[num]
                                   )
                               ],
                               tags = {
                                   "Name": f"{name}-private-rt"
                               })
        rt_private_association= aws.ec2.RouteTableAssociation(
            f"{name}-private-rt-association-{num}",
            route_table_id=rt_private.id,
            subnet_id= privateID[num]
        )
        rt_public = aws.ec2.RouteTable(f"{name}-public-rt-{num}",
                               vpc_id = vpc.id,
                               routes=[
                                   aws.ec2.RouteTableRouteArgs(
                                       cidr_block= "0.0.0.0/0",
                                       gateway_id= igw.id
                                   )
                               ],
                               tags = {
                                   "Name": f"{name}-public-rt"
                               })
        rt_public_association= aws.ec2.RouteTableAssociation(
            f"{name}-public-rt-association-{num}",
            route_table_id=rt_public.id,
            subnet_id= publicID[num]
        )
    
    
        vpce_id={}
        for a in range(len(privateID)):
            for count in session:
                n = count.split(".")[3]
                vpce=aws.ec2.VpcEndpoint(resource_name = f"{name}-{n}",
                                vpc_id=vpc.id,
                                subnet_ids= [privateID[a]],
                                auto_accept = True,
                                private_dns_enabled=True,
                                service_name= f"{count}",
                                vpc_endpoint_type="Interface",
                                security_group_ids=[sg["ssm-sg"]],
                                )
                vpce_id.update({f"{n}-id":vpce.id})
        
       
        pulumi.export("vpc arn", vpc.arn)
        pulumi.export("id", vpc.id)   
  
    
    
    
    
