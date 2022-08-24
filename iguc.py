import requests
from random_user_agent.user_agent import UserAgent as ua
from datetime import datetime
import sys

class IGUsernameChecker():

	def __init__(self, proxies=None):
		self.proxies = proxies
		print('Generating user agent ...')
		self.user_agent = ua().get_random_user_agent()
		print('Done')
		self.session = requests.session()
		self.url = "https://www.instagram.com/"
		self.login_url = "https://www.instagram.com/accounts/login/ajax/"
	
	def generate_password(self):
		return '#PWD_INSTAGRAM_BROWSER:0:{}:{}'.format(int(datetime.now().timestamp()), 'by#dhia#eddine')
	
	def is_real(self, username):
		data = {
			"enc_password":"",
			"username":"",
			"queryParams":"{}",
			"optIntoOneTap":"false",
			"stopDeletionNonce":"",
			"trustedDeviceRecords":"{}"
			}
		data.update({'username':username})
		data.update({'enc_password':self.generate_password()})
		try:
			res = self.session.post(self.login_url, headers=self.build_headers(self.user_agent), data=data, proxies=self.proxies).json()
			return res['user']
		except Exception as e : print(e)
		
		
	def build_headers(self, user_agent):
		cookies_c = dict(self.session.get(self.url, headers={'User-agent':self.user_agent}, proxies=self.proxies).cookies)
		csrftoken = cookies_c['csrftoken']
		headers = {
			"User-Agent": user_agent,
			"Accept": "*/*",
			"Accept-Language": "en-US,en;q=0.5",
			"Accept-Encoding": "gzip, deflate, br",
			"Connection": "keep-alive",
			"X-CSRFToken":csrftoken,
			"X-Requested-With": "XMLHttpRequest",
			"Referer": "https://www.instagram.com/",
			"Content-Type":"application/x-www-form-urlencoded"
		}
		
		return headers

iguc = IGUsernameChecker()
for username in sys.argv[1:]:
	print(username, iguc.is_real(username))


