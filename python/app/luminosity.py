from lib import backend
from lib import actuator
from lib import sensor
from lib.device import gpio
from .utils import dump_as_json
from threading import Condition as condition
import json
from threading import Timer as timer
import random

class luminosity(sensor):
	'''A smart-luminosity-sensor.
	The actuator part is to allow remote configuration.'''
	def __init__(self, i2c_addr, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._addr = i2c_addr
		self._timer : timer = None
		self._unit = 'lux'

	def get_lumi(self):
		return random.uniform(370, 420)

	def status_frame(self):
		return {
			'unitID': self._id,
			'value': self.get_lumi(),
			'unit': self._unit
		}

	def do_loop(self):
		# Take care to the closure here (ie. self._log)
		if self._log: self._log.info(f'luminosity {self._addr} enabled')
		def lumi():
			status = self.status_frame()
			if self._log: self._log.info(f'sending luminosity: {self.subject()}: {dump_as_json(status)}')
			self.send(status)
			self._timer = timer(10, lumi)
			self._timer.start()
		self._timer = timer(10, lumi)
		self._timer.start()
		self._backend.do_loop()

