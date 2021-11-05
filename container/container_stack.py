from aws_cdk import core as cdk
import yaml


class ContainerStack(cdk.Stack):

    def __init__(self,
                 scope: cdk.Construct,
                 construct_id: str,
                 cluster,  # add parameter
                 **kwargs) -> None:

        super().__init__(scope, construct_id, **kwargs)

        region = cdk.Stack.of(self).region

        common_yaml_file = './yaml-common/00_namespaces.yaml'
        region_yaml_file = f'./yaml-{region}/00_ap_nginx.yaml'

        # Read common yaml
        with open(common_yaml_file, 'r') as stream:
            common_yaml = yaml.load(stream, Loader=yaml.FullLoader)

        cluster.add_manifest(
            f'{construct_id}-common-yaml',
            common_yaml
        )

        # Read region yaml
        with open(region_yaml_file, 'r') as stream:
            region_yaml = yaml.load(stream, Loader=yaml.FullLoader)

        cluster.add_manifest(
            f'{construct_id}-{region}-yaml',
            region_yaml
        )
