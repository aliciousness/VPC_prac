import pulumi,json
import pulumi_aws as aws 

#BUG Trying to attach a role to an instance but i cant find an argument in pulumi to accept roles to instance, check back here 



def role(name,vpc_name):
    
    role_vpc = aws.iam.Role(f"EC2-role-{name}",
                            assume_role_policy=json.dumps({
                              "Version": "2012-10-17",
                              "Statement": [{
                                    "Action": 
                                        "sts:AssumeRole",
                                    "Principal": {
                                        "Service": "lambda.amazonaws.com",
                                    },
                                    "Effect": "Allow",
                                    "Sid": "",
            }]  
                            }))
   
    
    role_policy_attachment = aws.iam.RolePolicyAttachment(f"{name}-role-policy-attachment",
                                                          role=role_vpc.name,
                                                          policy_arn=aws.iam.ManagedPolicy.AMAZON_SSM_MANAGED_INSTANCE_CORE)
    
                                           