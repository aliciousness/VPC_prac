from rsa_python import rsa
import pulumi
import pulumi_aws as aws 



def CreateInstance(vpc_id,public_subnet_id,private_subnet_id,name,az,sg):
    user_data = open('/Users/richard/VPC_prac/VPC/user-data.txt','r').read()
    
    instance_profile = aws.iam.get_instance_profile(
                                                   name="SSMInstanceProfile-pulumi")
    key= aws.ec2.KeyPair(f"{name}-keypair",
                         key_name = f"{name}-keypair",
                         tags={
                             "Name": f"{name}-keypair"
                         },
                         public_key="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC33+tXxTIsZ/U3syGFUzCqJNWIIG7uK9uRQI6nxvKhGVGt4+GlUOuS95QmLzBiHgU7T+aAWgmRaDb6h0LqRUazCVkysaSMXctuRR9nKfpvxnH4UxLys/3l4Bz6rCk/jqV6cDDBTk5psbFstbfk+55JV1baa9EotzG3SNmI5cHMCtl4fWKqaDmj97GaTWXoYLtHtOOnYFoSH/4jYdkwZRVFKoA/8p9HnEzIoSQkQucVt2xdyRolZIsA6Re0ps1J+AGqd1N4SxbesBmf+RA8nyd0pv8MZDxHKdJz4msGga/uaBkHntMnZ0mZZwSiSokgXfD0GefxOqbhnJESYpknQXaFknp4PKyvBZACpakFlId1hIX0q+ny+gNS9VcE+WITFPc6ZOGEzE8ldD2k0GR6+InjNQR7QDXrTd0Bj0HRLnznSJQQQFU812TijvVdCXhN3d66fYCa3jvlfYH8gDsxqi2eBQWp5/UGbXMWwpeWCVCvB2Xc6YJrvAp+1QEPYQm5ksM= richard@Richards-Mac-mini.local")
    instance_public_id=[]
    instance_private_id=[]
    for n in range(az):
        instance_public= aws.ec2.Instance(f"{name}-public-instance",
                                   ami = "ami-0c02fb55956c7d316" #kernel5.10/x86
                                   ,
                                   instance_type="t2.micro",
                                   associate_public_ip_address= True,
                                   vpc_security_group_ids = [sg["sg_public_id"]],
                                   subnet_id= public_subnet_id[n],
                                   key_name= key.tags_all["Name"],
                                   user_data= user_data,
                                   tags={
                                      "Name": f"{name}-public-instance",
                                      "Subnet": f"{public_subnet_id}",
                                      "VPC": f"{vpc_id}",
                                      "Sg": f'{sg["sg_public_id"]}'
                                   }
                                   )
        instance_private= aws.ec2.Instance(f"{name}-private-instance",
                                   ami = "ami-0c02fb55956c7d316" #kernel5.10/x86
                                   ,
                                   instance_type="t2.micro",
                                   associate_public_ip_address= False,
                                   iam_instance_profile= instance_profile.role_name,
                                   vpc_security_group_ids = [sg["sg_private_id"]],
                                   subnet_id= private_subnet_id[n],
                                   key_name= key.tags_all["Name"],
                                   user_data= user_data,
                                   tags={
                                      "Name": f"{name}-private-instance",
                                      "Subnet": f"{private_subnet_id}",
                                      "VPC": f"{vpc_id}",
                                      "Sg": f'{sg["sg_private_id"]}'
                                   })
        instance_private_id.append(instance_private.id)
        instance_public_id.append(instance_public.id)
        
        pulumi.export("Instance(s)",{
            "private":{
                "instance arn": instance_private.arn,
                "instance id": instance_private.id,
                "instance profile": instance_profile.name
            },
            "public":{
                "instance arn": instance_public.arn,
                "instance id": instance_public.id,
            },
            "key":{
                "key-pair name": key.key_name,
                "key-pair id": key.key_pair_id,
                "Key-pair": key.public_key
            }
        })
    
    return {
        'sg':sg,
        'public_instance_id': instance_public_id,
        'private_instance_id ': instance_private_id,
        'keypair_id': key.key_pair_id
    }