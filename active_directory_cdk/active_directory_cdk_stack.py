from aws_cdk import (
    aws_directoryservice as directoryservice,
    aws_ec2 as ec2,
    aws_iam as iam,
    Stack,
    CfnOutput,
    Fn
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
            name=f"{ad_props['domain']}",
            password=f"{ad_props['adminpw']}",
            vpc_settings=directoryservice.CfnMicrosoftAD.VpcSettingsProperty(
                subnet_ids=ad_lookup,
                vpc_id=vpc.vpc_id
            ),

            # the properties below are optional
            create_alias=False,
            edition="Standard",
            enable_sso=False,
            short_name=f"{ad_props['short-name']}"
        )

        # Optional - create DHCP options

        cfn_dHCPOptions = ec2.CfnDHCPOptions(
            self,
            "ActiveDirectoryCfnDHCPOptions",
            domain_name=f"{ad_props['domain']}",
            domain_name_servers=[Fn.select(0,cfn_microsoft_aD.attr_dns_ip_addresses), Fn.select(1,cfn_microsoft_aD.attr_dns_ip_addresses)]
            )
        
        # Make sure we do not try this until the Active Directory has completed

        cfn_dHCPOptions.node.add_dependency(cfn_microsoft_aD)

        # Update VPC to use the DHCP options

        dhcp_options_associations = ec2.CfnVPCDHCPOptionsAssociation(
            self,
            'ActiveDirectoryCfnDHCPOptionsAssociation', 
            dhcp_options_id=cfn_dHCPOptions.ref, 
            vpc_id=vpc.vpc_id
            )

        # Create a new Role that can be used so that Windows instances can join your AWS Managed Microsoft AD domain

        ad_join_role = iam.Role(
            self,
            "JoinActiveDirectoryRole",
            role_name="ActiveDirectoryEC2IAMRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")
            )
        ad_join_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))
        ad_join_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMDirectoryServiceAccess"))

        # Not pretty, but hack from https://stackoverflow.com/questions/69308413/create-instanceprofile-with-cdk-and-python

        ec2instanceprofile = iam.CfnInstanceProfile(
            self,
            "EC2InstanceProfile",
            instance_profile_name="ActiveDirectoryEC2IAMRole",
            roles=["ActiveDirectoryEC2IAMRole"]
            )

        # Provision EC2 Windows Instance



        # Output key information

        CfnOutput(
            self,
            id="ActiveDirectoryId",
            value=cfn_microsoft_aD.attr_alias,
            description="Active Directory ID"
        )

        CfnOutput(
            self,
            id="IAMRoleJoiningActiveDirectory",
            value=ad_join_role.role_arn,
            description="Role used to Join Active Directory"
        )

        CfnOutput(
            self,
            id="ActiveDirectoryDNS-1",
            value=Fn.select(0,cfn_microsoft_aD.attr_dns_ip_addresses),
            description="Active Directory DNS IPs - First"
        )
        CfnOutput(
            self,
            id="ActiveDirectoryDNS-2",
            value=Fn.select(1,cfn_microsoft_aD.attr_dns_ip_addresses),
            description="Active Directory DNS IPs - Second"
        )






        
