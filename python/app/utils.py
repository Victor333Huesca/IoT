__all__ = ['dump_as_json', 'new_logger']

import sys
import json
import logging

# 1st operand works well for stdout but not for loggers, so force it to True
if sys.stdout.isatty():
	from pygments import highlight
	from pygments.lexers import JsonLexer
	from pygments.formatters import TerminalFormatter
	import coloredlogs
	def dump_as_json(data, *args, **kwargs):
		return highlight(json.dumps(data, *args, **kwargs), JsonLexer(), TerminalFormatter())[:-1]

	def new_logger(*args, name=None, level='DEBUG', **kwargs):
		logging.basicConfig(level=level)
		coloredlogs.install(level=level)
		return logging.getLogger(name)
else:
	def dump_as_json(data, *args, **kwargs):
		return json.dumps(data, *args, **kwargs)

	def new_logger(*args, name=None, level='DEBUG', **kwargs):
		logging.basicConfig(level=logging.getLevelName(level))
		return logging.getLogger(name)

