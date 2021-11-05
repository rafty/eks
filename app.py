#!/usr/bin/env python3
import os
from aws_cdk import core as cdk
from eks.eks_stack import EksStack
from master_vpc.vpc import VpcStack
from container.container_stack import ContainerStack

app = cdk.App()

account = os.getenv('CDK_DEFAULT_ACCOUNT')
primary_region = 'ap-northeast-1'
secondary_region = 'ap-northeast-2'

vpc_stack = VpcStack(
    scope=app,
    construct_id=f'eks-cluster-vpc-{primary_region}',
    env=cdk.Environment(account=account, region=primary_region)
)

eks_stack = EksStack(
    scope=app,
    construct_id=f'eks-cluster-stack-{primary_region}',
    env=cdk.Environment(account=account, region=primary_region),
    vpc=vpc_stack.vpc
)

container_stack = ContainerStack(
    scope=app,
    construct_id=f'eks-container-stack-{primary_region}',
    env=cdk.Environment(account=account, region=primary_region),
    cluster=eks_stack.cluster
)

app.synth()
