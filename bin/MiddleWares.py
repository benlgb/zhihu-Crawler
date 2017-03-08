# -*- coding: utf-8 -*-

import time
import gevent
import logging
import requests
from random import uniform
from src.MiddleWare import *
from conf.settings import *
from requests_oauthlib import OAuth1

# 防止短时间过快访问
class ShortTimePreProcess(PreProcess):
	def __init__(self, *args, **kwargs):
		self.time = time.time()
		super(self.__class__, self).__init__(*args, **kwargs)

	def process(self, id, req):
		deltatime = uniform(0.1, 0.5)
		if time.time() - self.time < deltatime:
			gevent.sleep(deltatime)
		self.time = time.time()
		return req

# 翻墙代理
class ProxiesPreProcess(PreProcess):
	proxies={
		'http': 'http://127.0.0.1:51754',
		'https': 'https://127.0.0.1:51754'
	}

	def process(self, id, req):
		req['args'] = req.get('args', {})
		req['args']['proxies'] = self.__class__.proxies
		return req

# API身份认证
class AuthPreProcess(PreProcess):
	consumer_key = '7cjhj2oyEv1CAkcQ414Qx4WmC'
	consumer_secret = 'UkVBF1OKaMRomJyGnQDHti9B6MC9gNhPNuAD4zSNiPS8ip7f9b'
	access_token_key = '831032425241206784-61gKvbULqvYCawcPDTWFfuZnWz5NNM3'
	access_token_secret = 'C1seiGpSzGayEicUuJDGQZJdcHKns59KHne4SHcyalKjk'
	auth = OAuth1(consumer_key, consumer_secret,
		access_token_key, access_token_secret)

	def process(self, id, req):
		req['args'] = req.get('args', {})
		req['args']['auth'] = self.__class__.auth
		return req

# 超时捕捉
class TimeoutPreProcess(PreProcess):
	def process(self, id, req):
		req['args'] = req.get('args', {})
		req['args']['timeout'] = 10
		return req

# 超时处理
class TimeoutError(Error):
	exception = requests.exceptions.ReadTimeout

	def error(self, e, id, req):
		req['times'] = req.get('times', 0) + 1
		e = 'Timeout(%(times)d): %(url)s' % req
		if req['times'] > MAX_TIMES:
			logging.error(e)
		else:
			logging.warning(e)
			self.input_queue.put_nowait(req)

# 连接失败
class ConnectionError(Error):
	exception = requests.exceptions.ConnectionError

	def error(self, e, id, req):
		req['times'] = req.get('times', 0) + 1
		e = 'Connect error(%(times)d): %(url)s' % req
		if req['times'] > MAX_TIMES:
			logging.error(e)
		else:
			logging.warning(e)
			self.input_queue.put_nowait(req)

# 请求错误
class StatusError(PostProcess):
	def process(self, id, req):
		e = '%d Status error: %s' % (req['response'].status_code, req['url'])
		if req['response'].status_code == 200:
			return req
		elif req['response'].status_code == 429:
			gevent.sleep(5)
			logging.warning(e)
			self.input_queue.put_nowait(req)
		else:
			req['question']['author_handle_count'] += 1
			logging.error(e)

# 编码设定
class CharacterPostProcess(PostProcess):
	def process(self, id, req):
		req['response'].encoding = 'utf-8'
		return req