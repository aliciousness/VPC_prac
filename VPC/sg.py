import pulumi
from pulumi_aws import ec2 

def Create_sg(vpc_id,name):
    sg_public = ec2.SecurityGroup(f"{name}-sg-public",
                                      description=f"This security group is for{name} in a public subnet",
                                      vpc_id= vpc_id,
                                      tags={
                                          "Name": f"{name}-sg-public"
                                      },
                                      ingress= ec2.SecurityGroupIngressArgs(
                                          description= "HTTP",
                                          protocol= "tcp",
                                          from_port=80,
                                          to_port= 80,
                                          cidr_blocks=["0.0.0.0/0"]
                                        ),
                                      ingress= ec2.SecurityGroupIngressArgs(
                                          description= "SSH",
                                          protocol= "tcp",
                                          from_port=22,
                                          to_port= 22,
                                          cidr_blocks=["0.0.0.0/0"]
                                        ),
                                      egress=ec2.SecurityGroupEgressArgs(
                                          description= "HTTPu",
                                          protocol= "tcp",
                                          from_port=80,
                                          to_port= 80,
                                          cidr_blocks=["0.0.0.0/0"]
                                        ),
                                      )
    sg_private = ec2.SecurityGroup(f"{name}-sg-private",
                                      description=f"This security group is for{name} in a private subnet",
                                      vpc_id= vpc_id,
                                      tags={
                                          "Name": f"{name}-sg-private"
                                      },
                                      ingress= ec2.SecurityGroupIngressArgs(
                                          description= "",
                                          protocol= "HTTP tcp",
                                          from_port=80,
                                          to_port= 80,
                                          security_groups= [sg_public.id]
                                        )
                                      )
    return{
        "sg_public_id": sg_public.id,
        "sg_private_id": sg_private.id
    }