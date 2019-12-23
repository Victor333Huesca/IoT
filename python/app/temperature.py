from lib import backend
from lib import actuator
from lib import sensor
from lib.device import gpio
from .utils import dump_as_json
from threading import Condition as condition
from threading import Timer as timer
import json

class temperature(sensor):
	'''A smart-temperature sensor.'''
	def __init__(self, pin_up, pin_down, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._pin_up = pin_up
		self._pin_down = pin_down
		gpio.setup(pin_up, gpio.OUT)
		gpio.setup(pin_up, gpio.OUT)
		self._status = 'close'
		self._order = 'idle'
		self._timer : timer = None
		self._timer_cond = condition()

	def on_complete(self, status):
		if self._log: self._log.info(f'timers\'s up! new status: {status}')
		self._status = status
		status = self.status_frame()
		if self._log: self._log.info(f'order complete, sending new status on topic {self.subject()}: {dump_as_json(status)}')
		self.send(status)


	def up(self):
		if self._order == 'up':
			return
		self._order = 'up'
		if self._status != 'open':
			self._status = 'between'
			self._timer_cond.acquire()
			if self._timer:
				self._timer.cancel()
			self._timer = timer(10, self.on_complete, ('open',))
			self._timer.start()
			self._timer_cond.release()
			gpio.output(self._pin_up, gpio.LOW)
			gpio.output(self._pin_up, gpio.HIGH)

	def down(self):
		if self._order == 'down':
			return
		self._order = 'down'
		if self._status != 'close':
			self._status = 'between'
			self._timer_cond.acquire()
			if self._timer:
				self._timer.cancel()
			self._timer = timer(30, self.on_complete, ('close',))
			self._timer.start()
			self._timer_cond.release()
			gpio.output(self._pin_up, gpio.HIGH)
			gpio.output(self._pin_up, gpio.LOW)

	def stop(self):
		if self._order == 'idle':
			return
		self._order == 'idle'
		self._timer_cond.acquire()
		if self._timer:
			self._timer.cancel()
		self._timer = None
		self._timer_cond.release()
		gpio.output(self._pin_up, gpio.HIGH)
		gpio.output(self._pin_up, gpio.HIGH)

	def status_frame(self):
		return {
			'unitID': self._id,
			'status': self._status,
			'order': self._order
		}

	def do_loop(self):
		# Take care to the closure here (ie. self._log)
		def recv(client, userdata, msg):
			payload = json.loads(msg.payload.decode())
			if self._log: self._log.info(f'new command: {msg.topic}: {dump_as_json(payload)}')
			if payload['dest'] in ('all', self._id):
				status = self.status_frame()
				if payload['order'] in ('up', 'UP'):
					self.up()
				elif payload['order'] in ('down', 'DOWN'):
					self.down()
				elif payload['order'] in ('stop', 'STOP'):
					self.stop()
				elif payload['order'] in ('status', 'STATUS'):
					pass # we would do it anyway
				else:
					if self._log: self._log.warn(f'unknown order: { payload["order"] }')
				if self._log: self._log.info(f'sending old status: {self.subject()}: {dump_as_json(status)}')
				self.send(status)

		self.on_recv(recv)
		self._backend.do_loop()
