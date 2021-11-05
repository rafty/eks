#!/usr/bin/env python3
import os
from aws_cdk import core as cdk
from eks.eks_stack import EksStack
from master_vpc.vpc import VpcStack


app = cdk.App()

account = os.getenv('CDK_DEFAULT_ACCOUNT')
master_region = 'ap-northeast-1'
secondary_region = 'ap-northeast-2'

vpc_stack = VpcStack(
    scope=app,
    construct_id=f'eks-cluster-vpc-{master_region}',
    env=cdk.Environment(account=account, region=master_region)
)

eks_stack = EksStack(
    scope=app,
    construct_id=f'eks-cluster-stack-{master_region}',
    env=cdk.Environment(account=account, region=master_region),
    vpc=vpc_stack.vpc
)

app.synth()
