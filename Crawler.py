# -*- coding: utf-8 -*-

import os
import gevent
import logging, logging.config
from gevent.queue import JoinableQueue

from conf.settings import *
from src.RequestController import RequestController
from bin.DataController import DataController

# 启用日志
if not os.path.isdir('log'):
	os.makedirs('log')
logging.config.fileConfig('conf/logger.conf')

class Crawler(object):
	def __init__(self):
		self.input_queue = JoinableQueue()
		self.output_queue = JoinableQueue()

	def run(self):
		self.request_controller = RequestController(self.input_queue, 
			self.output_queue, MIDDLEWARES)
		self.data_controller = DataController(self.input_queue,
			self.output_queue, self.request_controller)
		gevent.joinall([gevent.spawn(self.request_controller, i) 
			for i in range(REQUEST_COUNT)] + [gevent.spawn(self.data_controller)])

if __name__ == '__main__':
	Crawler().run()