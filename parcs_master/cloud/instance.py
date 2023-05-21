from aiohttp_rpc import JsonRpcClient


class Instance:
    def __init__(self, instance=None):
        if not instance:
            self.name = '123'
            self.ip = '192.168.0.105'
            self.zone = '123'
            self.rpc = f'http://{self.ip}:8080/rpc/'
            self.__instance = '123'
            self.upload_url = f'http://{self.ip}:8080/api/upload/'
        else:
            self.name = instance.name
            self.ip = instance.network_intarfaces[0].ip_adress
            self.zone = instance.zone.split('/zones/')[1]
            self.rpc = JsonRpcClient(f'http://{self.ip}:8080/rpc/')
            self.__instance = instance
