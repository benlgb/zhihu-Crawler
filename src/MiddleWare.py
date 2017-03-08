# -*- coding: utf-8 -*-

import logging
import traceback

class MiddleWare(object):
	def __init__(self, fn, input_queue, output_queue):
		self.fn = fn
		self.input_queue = input_queue
		self.output_queue = output_queue

	def __call__(self, id, req):
		if req:
			res = self.ware(id, req)
			if res:
				return res

	def ware(self, id, req):
		return self.fn(id, req)

class PreProcess(MiddleWare):
	def ware(self, id, req):
		res = self.process(id, req)
		if res:
			return self.fn(id, req)

	def process(self, id, req):
		return req

class PostProcess(MiddleWare):
	def ware(self, id, req):
		res = self.fn(id, req)
		if res:
			return self.process(id, req)

	def process(self, id, req):
		return req

class Error(MiddleWare):
	exception = Exception

	def ware(self, id, req):
		try:
			return self.fn(id, req)
		except self.__class__.exception, e:
			self.error(e, id, req)

	def error(self, e, id, req):
		logging.error('%s: %s' % (e.__class__.__name__, e))
		traceback.print_exc()