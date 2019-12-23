from .device import device

class actuator(device):
	'''Common class for all acurators'''
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def subscribe(self):
		self._backend.subscribe(f'{self.subject()}/command')

	def on_recv(self, callback):
		self._backend.on_recv(callback)
