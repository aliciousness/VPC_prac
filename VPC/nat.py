import pulumi 
from pulumi_aws import get_availability_zones
import pulumi_aws as aws 

def Create_nat(subnet_id,name):
    public_nat_eip = aws.ec2.Eip(f'{name}-public-eip',
                                 tags={
                                     "Name": f"{name}-public-eip"
                                 })
    
    for n in range(len(subnet_id)):
        aws.ec2.nat_gateway(f"{name}-natgateway-{n}",
                    subnet_id= subnet_id[n],
                    allocation_id=public_nat_eip.id,
                    tags={
                        "Name": f"{name}-natgateway-{n}"
                    })