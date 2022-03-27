from unicodedata import name
import pulumi
from pulumi_aws import ec2 


def Create_sg(vpc_id,name):
    sg_public = ec2.SecurityGroup(f"{name}-sg-public",
                                      description=f"This security group is for{name} in a public subnet",
                                      vpc_id= vpc_id,
                                      tags={
                                          "Name": f"{name}-sg-public"
                                      },
                                      ingress= [
                                        ec2.SecurityGroupIngressArgs(
                                          description= "HTTP",
                                          protocol= "tcp",
                                          from_port=80,
                                          to_port= 80,
                                          cidr_blocks=["0.0.0.0/0"]
                                        ),
                                        ec2.SecurityGroupIngressArgs(
                                          description= "SSH",
                                          protocol= "tcp",
                                          from_port=22,
                                          to_port= 22,
                                          cidr_blocks=["0.0.0.0/0"]
                                        )],
                                      egress=[
                                        ec2.SecurityGroupEgressArgs(
                                          description= "HTTP",
                                          protocol= "tcp",
                                          from_port=80,
                                          to_port= 80,
                                          cidr_blocks=["0.0.0.0/0"]
                                        )],
                                      )
    sg_private = ec2.SecurityGroup(f"{name}-sg-private",
                                      description=f"This security group is for{name} in a private subnet",
                                      vpc_id= vpc_id,
                                      tags={
                                          "Name": f"{name}-sg-private"
                                      },
                                      )
    ssm_session_sg = ec2.SecurityGroup(f"ssm-session-vpce-sg-{name}",
                                    description="SG for ssm session vpce",
                                    vpc_id=vpc_id,
                                    ingress=[ec2.SecurityGroupIngressArgs(
                                        description="HTTPS ipv4",
                                        from_port=443,
                                        to_port=443,
                                        protocol="tcp",
                                        cidr_blocks=['0.0.0.0/0']
                                    ),
                                             ec2.SecurityGroupIngressArgs(
                                        description="HTTPS ipv6",
                                        from_port=443,
                                        to_port=443,
                                        protocol="tcp",
                                        ipv6_cidr_blocks=['::/0']
                                    )
                                             ],
                                    egress=[ec2.SecurityGroupIngressArgs(
                                        description="HTTPS ipv4",
                                        from_port=443,
                                        to_port=443,
                                        protocol="tcp",
                                        cidr_blocks=['0.0.0.0/0']
                                    )],
                                    tags={
                                        "Name": f'{name}-ssm-vpce-sg'
                                    }
                                    )
    return{
        "sg_public_id": sg_public.id,
        "sg_private_id": sg_private.id,
        "ssm-sg": ssm_session_sg.id
    }