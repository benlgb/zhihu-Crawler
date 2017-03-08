# -*- coding: utf-8 -*-

import gevent
import requests
from conf.settings import *
from gevent import monkey
monkey.patch_socket()
monkey.patch_ssl()

class RequestController(object):
	def __init__(self, input_queue, output_queue, middlewares=()):
		self.input_queue = input_queue
		self.output_queue = output_queue
		self.middlewares = middlewares
		for middleware in self.middlewares:
			self.request = middleware(self.request, input_queue, output_queue)
		self.session = requests.Session()
		self.session.headers.update(REQUEST_HEADERS)
		self.running = True

	def __call__(self, id):
		while self.running:
			if self.input_queue.empty():
				gevent.sleep(0)
				continue
			req = self.input_queue.get_nowait()
			request = self.request
			for middleware in req.get('middlewares', ()):
				request = middleware(request, self.input_queue, self.output_queue)
			res = request(id, req)
			self.input_queue.task_done()
			if res: self.output_queue.put_nowait(res)

	def request(self, id, req):
		method = req.get('method', 'get').lower()
		if method == 'get':
			res = self.session.get(req['url'], **req['args'])
		elif method == 'post':
			res = self.session.post(req['url'], **req['args'])
		req['response'] = res
		return req

	def close(self):
		self.running = False