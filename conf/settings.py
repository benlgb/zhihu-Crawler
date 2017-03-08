# -*- coding: utf-8 -*-

# 最高重复访问数
MAX_TIMES = 5

# 最高同时访问数
REQUEST_COUNT = 5

# 请求头参数
REQUEST_HEADERS = {
	'Host': 'www.zhihu.com',
	'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
}

from bin.MiddleWares import *

# 中间件
MIDDLEWARES = (
		ShortTimePreProcess,	# 防止短时间过快访问
		# ProxiesPreProcess,	# 翻墙代理
		# AuthPreProcess,		# OAuth1身份认证
		TimeoutPreProcess,		# 超时检测
		CharacterPostProcess,	# 设置默认编码
		TimeoutError,			# 超时错误处理
		ConnectionError,		# 连接错误处理
		StatusError,			# 状态码异常
		Error,					# 异常捕获
	)