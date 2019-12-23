from .backend import backend
from paho.mqtt.client import Client as mqtt_client

class mqtt(backend):
	'''MQTT backend'''
	def __init__(self, addr=None, port=1883):
		super().__init__(addr, port)
		self._conn = mqtt_client()
		if addr and port:
			self._conn.connect(addr, port, 60)

	def __repr__(self):
		return f'mqtt ({hex(hash(self._conn))})'

	def send(self, topic, data=None, *args, **kwargs):
		self._conn.publish(topic, data, *args, **kwargs)

	def connect(self, addr, port):
		super().connect(addr, port)
		self._conn.connect(addr, port, 60)

	def send_to(self, data, addr, port, reset=False):
		self.connect(addr, port)
		self._conn.publish(data)
		if reset:
			self._addr = None
			self._port = None

	def subscribe(self, subject):
		super().subscribe(subject)
		self._conn.subscribe(subject)

	def do_loop(self):
		self._conn.loop_start()

	def on_recv(self, callback):
		self._conn.on_message = callback

	def enable_logger(self, logger):
		self._conn.enable_logger(logger)