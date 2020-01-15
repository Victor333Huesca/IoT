import logging
import sys

sys.path[0] = sys.path[0] + '/..'
from app import luminosity
from lib import mqtt, gpio

from app.utils import new_logger
logger = new_logger('shutter', level='DEBUG')

gpio.setmode(gpio.BCM)
shutter_mqtt = mqtt('192.168.0.220')
lumi1 = luminosity(1, '1r1', '014', 'luminosity', '1', log=logger, be=shutter_mqtt)
lumi2 = luminosity(2, '1r1', '014', 'luminosity', '2', log=logger, be=shutter_mqtt)

lumi1.enable_logger(logger)
lumi1.do_loop()

lumi2.enable_logger(logger)
lumi2.do_loop()

from time import sleep
sleep(60*60)
