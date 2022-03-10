import ipaddress
from pulumi_aws import get_availability_zones

i = list(ipaddress.ip_network('10.0.0.0/16').subnets(new_prefix=24))




for count in range(2):
    print(i[count])
    print(i[count])

    
