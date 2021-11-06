#!/usr/bin/env python3
import os
from aws_cdk import core as cdk
from eks.eks_stack import EksStack
from vpc.vpc import VpcStack
from container.container_stack import ContainerStack

app = cdk.App()

account = os.getenv('CDK_DEFAULT_ACCOUNT')
primary_region = 'ap-northeast-1'
secondary_region = 'ap-northeast-2'

# -------------------------------------------------------------
# Primary VPC
# -------------------------------------------------------------

primary_vpc_stack = VpcStack(
    scope=app,
    construct_id=f'eks-cluster-vpc-{primary_region}',
    env=cdk.Environment(account=account, region=primary_region)
)

primary_eks_stack = EksStack(
    scope=app,
    construct_id=f'eks-cluster-stack-{primary_region}',
    env=cdk.Environment(account=account, region=primary_region),
    vpc=primary_vpc_stack.vpc
)

primary_container_stack = ContainerStack(
    scope=app,
    construct_id=f'eks-container-stack-{primary_region}',
    env=cdk.Environment(account=account, region=primary_region),
    cluster=primary_eks_stack.cluster
)

# -------------------------------------------------------------
# Secondary VPC
# -------------------------------------------------------------

secondary_vpc_stack = VpcStack(
    scope=app,
    construct_id=f'eks-cluster-vpc-{secondary_region}',
    env=cdk.Environment(account=account, region=secondary_region)
)

secondary_eks_stack = EksStack(
    scope=app,
    construct_id=f'eks-cluster-stack-{secondary_region}',
    env=cdk.Environment(account=account, region=secondary_region),
    vpc=secondary_vpc_stack.vpc
)

secondary_container_stack = ContainerStack(
    scope=app,
    construct_id=f'eks-container-stack-{secondary_region}',
    env=cdk.Environment(account=account, region=secondary_region),
    cluster=secondary_eks_stack.cluster
)


app.synth()
