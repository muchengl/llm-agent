import json
import os
import logging
from datetime import datetime

from constructs import Construct
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
)

public_ssh_key = ""

logger = logging.getLogger(__name__)
current_time = datetime.now()

security_group_name = "llm-agent"
security_group_description  = "state driven llm-agent"
security_group_ip_range = os.getenv("IP_RANGE")

ec2_name = "WebArenaServer"
ec2_key_pair_name = "lm-agent-key-pair"
ec2_size = "t3a.xlarge"

eip_name = "WebArenaCDN"

class WebArenaEc2Stack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Get Default VPC
        vpc = ec2.Vpc.from_lookup(self, "DefaultVPC", is_default=True)

        # 1. Create Security Group
        security_group = ec2.SecurityGroup(
            self, "SecurityGroup",
            vpc=vpc,
            security_group_name=security_group_name,
            description=security_group_description,
            allow_all_outbound=True
        )

        security_group.add_ingress_rule(
            peer=ec2.Peer.ipv4(security_group_ip_range),
            connection=ec2.Port.all_traffic(),
            description=f"Allow all traffic from {security_group_ip_range}"
        )

        global public_ssh_key
        if public_ssh_key is "":
            public_ssh_key = self.get_first_ssh_public_key()
            if public_ssh_key is None:
                return

        key_pair = ec2.CfnKeyPair(
            self,
            "KeyPair",
            key_name=ec2_key_pair_name,
            public_key_material=public_ssh_key
        )

        # WebArena
        ami = ec2.MachineImage.lookup(
            name="webarena"
        )

        instance = ec2.Instance(
            self,
            ec2_name,
            instance_type=ec2.InstanceType(ec2_size),
            machine_image=ami,
            vpc=vpc,
            security_group=security_group,
            key_name=ec2_key_pair_name
        )

        eip = ec2.CfnEIP(
            self,
            eip_name,
            domain="vpc",
            instance_id=instance.instance_id
        )

        # Collect all the information into a dictionary
        deployment_info = {
            "security_group": {
                "name": security_group_name,
                "description": security_group_description,
                "id": security_group.security_group_id,
                "ip_range": security_group_ip_range
            },
            "key_pair": {
                "key_name": ec2_key_pair_name
            },
            "instance": {
                "instance_name": ec2_name,
            }
        }


        # Save the information to a JSON file named 'spec.json'
        with open('spec.json', 'w') as spec_file:
            json.dump(deployment_info, spec_file, indent=4)

        logger.info(f"Deployment information saved to spec.json: {json.dumps(deployment_info, indent=4)}")


    def get_ssh_public_keys(self):
        ssh_dir = os.path.expanduser("~/.ssh")

        if not os.path.exists(ssh_dir):
            print("can't find ssh dir")
            return None

        public_keys = []

        for filename in os.listdir(ssh_dir):
            if filename.endswith(".pub"):
                pub_key_path = os.path.join(ssh_dir, filename)
                with open(pub_key_path, 'r') as file:
                    public_keys.append(file.read().strip())

        all_public_keys = "\n".join(public_keys)
        return all_public_keys


    def get_first_ssh_public_key(self):
        ssh_dir = os.path.expanduser("~/.ssh")

        if not os.path.exists(ssh_dir):
            print("can't find ssh dir")
            return None

        for filename in os.listdir(ssh_dir):
            if filename.endswith(".pub"):
                pub_key_path = os.path.join(ssh_dir, filename)
                with open(pub_key_path, 'r') as file:
                    public_key = file.read().strip()
                return public_key

        print("can't find ssh key")
        return None
