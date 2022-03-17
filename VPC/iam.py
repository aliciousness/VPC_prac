from inspect import ArgInfo
import pulumi,json
import pulumi_aws as aws 



def CreateRole(name):
    
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
    
    instance_profile = aws.iam.InstanceProfile("instance-role",
                                               name_prefix=f"{name}",
                                               path="/",
                                               role= role_vpc.name)
    
    pulumi.export("IAM",
                  {
                      "instance_profile": instance_profile.arn,
                      "role_arn": role_vpc.arn,
                  })
    
    return instance_profile.name
    
                                           