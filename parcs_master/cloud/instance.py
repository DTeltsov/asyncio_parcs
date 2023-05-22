class Instance:
    def __init__(self, instance=None):
        self.name = instance.name
        self.ip = instance.network_interfaces[0].network_i_p
        self.zone = instance.zone.split('/zones/')[1]
        self.rpc = f'http://{self.ip}:8080/rpc/'
        self.upload_url = f'http://{self.ip}:8080/api/upload/'
        self.__instance = instance
