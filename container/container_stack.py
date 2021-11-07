from aws_cdk import core as cdk
from aws_cdk import aws_eks
import yaml
from util.read_manifest import read_manifests_from_directory


class ContainerStack(cdk.Stack):

    def __init__(self,
                 scope: cdk.Construct,
                 construct_id: str,
                 cluster: aws_eks.Cluster,  # add parameter
                 **kwargs) -> None:

        super().__init__(scope, construct_id, **kwargs)

        region = cdk.Stack.of(self).region

        common_yaml_file = './yaml-common/00_namespaces.yaml'
        region_yaml_file = f'./yaml-{region}/00_ap_nginx.yaml'
        common_manifest_directory = './yaml-common/'
        region_manifest_directory = f'./yaml-{region}/'

        # Read common yaml
        # with open(common_yaml_file, 'r') as stream:
        #     common_docs = list(
        #         yaml.load_all(stream, Loader=yaml.FullLoader))
        #
        # for doc in common_docs:
        #     cluster.add_manifest(
        #         f'{doc["metadata"]["name"]}-common-yaml',
        #         doc
        #     )
        read_manifests_from_directory(common_manifest_directory, cluster)

        # Read region yaml
        # with open(region_yaml_file, 'r') as stream:
        #     region_yaml = yaml.load(stream, Loader=yaml.FullLoader)
        #
        # cluster.add_manifest(
        #     f'{construct_id}-{region}-yaml',
        #     region_yaml
        # )

        read_manifests_from_directory(region_manifest_directory, cluster)

        # Helm Chart - flux CD
        cluster.add_helm_chart(
            id='flux',
            repository='https://charts.fluxcd.io',
            chart='flux',
            release='flux',
            values={
                'git.url': 'git@github.com:org/repo'
            }
        )
