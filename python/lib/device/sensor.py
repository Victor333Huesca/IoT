from .device import device
import json

class sensor(device):
	'''Common class for all sensors'''
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def send(self, data=None, *args, **kwargs):
		self._backend.send(self.subject(), json.dumps(data), *args, **kwargs)
