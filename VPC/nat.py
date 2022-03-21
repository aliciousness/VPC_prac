import pulumi 
import pulumi_aws as aws 

def Create_nat(subnet_id,name):
    nat_gateway_id = []
   
    
    #create eip and nat 
    for n in range(len(subnet_id)):
        nat_eip = aws.ec2.Eip(f'{name}-eip',
                                    tags={
                                        "Name": f"{name}-public-eip"
                                    })
        
        
        nat_gateway=aws.ec2.NatGateway(f"{name}-natgateway-{n}",
                    subnet_id= subnet_id[n],
                    allocation_id=nat_eip.allocation_id,
                    tags={
                        "Name": f"{name}-natgateway-{n}"
                    })
        nat_gateway_id.append(nat_gateway.id)
    return nat_gateway_id