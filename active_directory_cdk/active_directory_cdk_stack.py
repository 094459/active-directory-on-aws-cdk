from aws_cdk import (
    aws_directoryservice as directoryservice,
    aws_ec2 as ec2,
    Stack,
    CfnOutput
)
from constructs import Construct

class ActiveDirectoryCdkStack(Stack):

    def __init__(self, scope: Construct, id: str, vpc, ad_props, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Grab Subnet IDs from VPC

        ad_subnets = vpc.select_subnets(
            subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
        )
        ad_lookup = []

        for subnet in ad_subnets.subnets:
            ad_lookup.append(subnet.subnet_id)

        # Create an instance of Active Directory

        cfn_microsoft_aD = directoryservice.CfnMicrosoftAD(
            self,
            "DemoMicrosoftAD",
            name="devad-ricsue.dev",
            password=f"{ad_props['adminpw']}",
            vpc_settings=directoryservice.CfnMicrosoftAD.VpcSettingsProperty(
                subnet_ids=ad_lookup,
                vpc_id=vpc.vpc_id
            ),

            # the properties below are optional
            create_alias=False,
            edition="Standard",
            enable_sso=False,
            short_name="devad"
        )

        CfnOutput(
            self,
            id="ActiveDirectoryId",
            value=cfn_microsoft_aD.attr_alias,
            description="Active Directory ID"
        )

        # getAtt("DnsIpAddresses"




        
