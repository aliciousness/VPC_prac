import pulumi 
import pulumi_aws as aws 

def Create_nat(subnet_id,name):
    nat_gateway_id = []
    nat_eip_id =[]
    
    #create eip and nat 
    for n in range(len(subnet_id)):
        nat_eip = aws.ec2.Eip(f'{name}-public-eip',
                                    tags={
                                        "Name": f"{name}-public-eip"
                                    })
        nat_eip_id.append(nat_eip.id)
        
        nat_gateway=aws.ec2.NatGateway(f"{name}-natgateway-{n}",
                    subnet_id= subnet_id[n],
                    allocation_id=nat_eip_id[n],
                    tags={
                        "Name": f"{name}-natgateway-{n}"
                    })
        nat_gateway_id.append(nat_gateway.id)
        
    pulumi.export("NAT", {
        "ID": nat_gateway.id,
        "private_ip":nat_gateway.private_ip,
        "public": nat_gateway.public_ip
    })
    
    return nat_gateway_id