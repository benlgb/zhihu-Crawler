# -*- coding: utf-8 -*-

import os
import json
import requests

for question_id in os.listdir('data')
	path = os.path.join('data', question_id)
	for answers in os.listdir(path):
		answers_path = os.path.join(path, answers)
		with open(answers_path) as f:
			
# url = 'https://www.zhihu.com/node/QuestionAnswerListV2'
# data = {
# 	'method': 'next',
# 	'params': json.dumps({
# 		'url_token': 36011633,
# 		'pagesize': 10,
# 		'offset': 20
# 	})
# }
# REQUEST_HEADERS = {
# 	'Upgrade-Insecure-Requests': '1',
# 	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
# }
# res = requests.post(url, data=data, headers=REQUEST_HEADERS)

# with open('test.html', 'w+') as f:
# 	f.write(res.text)