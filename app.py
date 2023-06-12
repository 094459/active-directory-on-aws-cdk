#!/usr/bin/env python3
import os

import aws_cdk as cdk

from active_directory_cdk.active_directory_cdk_stack import ActiveDirectoryCdkStack
from active_directory_cdk.active_directory_vpc_cdk_stack import ActiveDirectoryVPCCdkStack

env_EU=cdk.Environment(region="eu-west-1", account="xxxxx")
ad_props = {
    'adminpw': 'xxxxx',
    'domain' : 'devad.ricsue.dev',
    'short-name' : 'devad'
    }

app = cdk.App()

ad_vpc = ActiveDirectoryVPCCdkStack(
    scope=app,
    id="ad-demo-vpc",
    env=env_EU
)
ad_svc = ActiveDirectoryCdkStack(
    scope=app,
    ad_props=ad_props,
    vpc=ad_vpc.vpc,
    id="ad-demo-svc",
    env=env_EU
)

app.synth()
