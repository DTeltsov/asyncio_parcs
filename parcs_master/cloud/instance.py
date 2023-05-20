
class Instance:
    def __init__(self, instance):
        self.name = instance.name
        self.ip = '10.194.0.5'
        self.zone = instance.zone.split('/zones/')[1]
        self.__instance = instance

    @property
    def upload_url(self):
        return f'https://{self.ip}:8000/api/file/'

    @property
    def upload_url(self):
        return f'https://{self.ip}:8000/api/execute/'
