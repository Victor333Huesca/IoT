from abc import ABC, abstractmethod

class backend(ABC):
	'''Common interface for all backend'''
	def __init__(self, addr=None, port=4242):
		self._addr = addr
		self._port = port

	@abstractmethod
	def connect(self, addr, port):
		self._addr = addr
		self._port = port

	@abstractmethod
	def send(self, data):
		pass

	@abstractmethod
	def send_to(self, data, addr, port):
		pass

	@abstractmethod
	def on_recv(self, callback):
		pass

	@abstractmethod
	def subscribe(self, subject):
		pass

	@abstractmethod
	def enable_logger(self, logger):
		pass
