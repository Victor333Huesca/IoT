import json
from ..network import backend

class device:
	'''
	Common class for all devices
	'''
	def __init__(self, building, room, class_topic, uid, be: backend=None, log=None):
		# Parameters
		self._building = building
		self._room = room
		self._class = class_topic
		self._id = uid
		# Internals
		self._backend = be
		self._log = log

	def __repr__(self):
		return 'device'
		return f'device \'{self._building}/{self._room}/{self._class}/{self._id}\' ({hex(hash(self))})'

	def subject(self):
		return f'{self._building}/{self._room}/{self._class}'

	def set_backend(self, be: backend):
		self._backend = be

	def enable_logger(self, logger):
		self._backend.enable_logger(logger)
