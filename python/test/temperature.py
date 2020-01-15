import logging
import sys

sys.path[0] = sys.path[0] + '/..'
from app import temperature
from lib import mqtt, gpio

from app.utils import new_logger
logger = new_logger('shutter', level='DEBUG')

gpio.setmode(gpio.BCM)
shutter_mqtt = mqtt('192.168.0.220')
temp1 = temperature(1, '1r1', '014', 'temperature', '1', log=logger, be=shutter_mqtt)
temp2 = temperature(2, '1r1', '014', 'temperature', '2', log=logger, be=shutter_mqtt)

temp1.enable_logger(logger)
temp1.do_loop()

temp2.enable_logger(logger)
temp2.do_loop()

from time import sleep
sleep(60*60)
