import logging
import sys

sys.path[0] = sys.path[0] + '/..'
from app import shutter
from lib import mqtt, gpio

from app.utils import new_logger
logger = new_logger('shutter', level='DEBUG')

gpio.setmode(gpio.BCM)
shutter_mqtt = mqtt('192.168.0.220')
shutter_back = shutter(27, 24, '1r1', '014', 'shutter', 'back', log=logger, be=shutter_mqtt)
shutter_front = shutter(17, 23, '1r1', '014', 'shutter', 'front', log=logger, be=shutter_mqtt)
shutter_center = shutter(16, 20, '1r1', '014', 'shutter', 'center', log=logger, be=shutter_mqtt)

shutter_front.enable_logger(logger)
shutter_front.subscribe()
shutter_front.do_loop()

shutter_back.enable_logger(logger)
shutter_back.subscribe()
shutter_back.do_loop()

from time import sleep
sleep(60*60)

