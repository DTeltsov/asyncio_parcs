import asyncio
from abc import ABC, abstractmethod

from google.cloud import compute_v1
from google.oauth2 import service_account

from .consts import STARTUP_SCRIPT
from .instance import Instance


class AbstractCloudController(ABC):
    @abstractmethod
    def create_instance(self):
        pass

    @abstractmethod
    def delete_instance(self, instance_name):
        pass

    @abstractmethod
    def get_instances(self):
        pass


class GoogleCloudController(AbstractCloudController):
    def __init__(self, creds):
        self.__credentials = service_account.Credentials.from_service_account_file(creds)

        # init clients
        self.__compute_client = compute_v1.InstancesClient(credentials=self.__credentials)
        self.__regions_client = compute_v1.RegionsClient(credentials=self.__credentials)

        # init variables for operations
        self.__project = self.__credentials.project_id
        # this is done only because of vm quota for region and for user comfort
        self.__regions = (region.name for region in self.__regions_client.list(project=self.__project).items)
        self.__region = next(self.__regions)

    @property
    def __zone(self):
        return f'{self.__region}-a'

    @property
    async def __instances(self):
        return {
            instance.name: Instance(instance)
            for instance in await self.__get_instances()
        }

    @property
    def __loop(self):
        return asyncio.get_running_loop()

    async def get_instances(self):
        return list((await self.__instances).values())

    async def __get_instances(self):
        regions = await self.__loop.run_in_executor(
            None,
            lambda: self.__compute_client.aggregated_list(project=self.__project)
        )
        existing_instances = []
        for region in regions:
            if region[1].instances:
                for instance in region[1].instances:
                    if instance.status in ['RUNNING', 'STAGING']:
                        existing_instances.append(instance)
        return existing_instances

    async def create_instance(self):
        instance_number = len(await self.__instances) + 1
        name = f'instance-{instance_number}'
        config = compute_v1.Instance(
            name=name,
            machine_type=f'zones/{self.__zone}/machineTypes/n1-standard-1',
            disks=[
                compute_v1.AttachedDisk(
                    boot=True,
                    auto_delete=True,
                    initialize_params=compute_v1.AttachedDiskInitializeParams(
                        source_image='projects/debian-cloud/global/images/family/debian-11'
                    )
                )
            ],
            network_interfaces=[
                compute_v1.NetworkInterface(
                    network="global/networks/default",
                    access_configs=[
                        compute_v1.AccessConfig(name='External NAT', network_tier='PREMIUM')
                    ]
                )
            ],
            metadata=compute_v1.Metadata(
                items=[
                    compute_v1.Items(
                        key="startup-script",
                        value=STARTUP_SCRIPT
                    )
                ]
            )
        )
        await self.__loop.run_in_executor(
            None,
            lambda: self.__compute_client.insert(
                project=self.__project,
                zone=self.__zone,
                instance_resource=config
            )
        )
        if len(await self.__instances) % 4 == 0:
            self.__region = next(self.__regions)
        return await self.__instances

    async def delete_instance(self, instance_name):
        zone = (await self.__instances)[instance_name].zone
        await self.__loop.run_in_executor(
            None,
            lambda: self.__compute_client.delete(
                project=self.__project,
                zone=zone,
                instance=instance_name
            )
        )
