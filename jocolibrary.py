#!python3
#requests_login.py is a code snippet/script you can customise to do a request get of a site behind a login.
#For this example file I'm pulling down my home page post listing on freecycle.org.

import requests
from bs4 import BeautifulSoup

#This URL will be the URL that your login form points to with the "action" tag.
POST_LOGIN_URL = 'https://jocolibrary.bibliocommons.com/user/login'

#This URL is the page you actually want to pull down with requests.
REQUEST_URL = 'https://jocolibrary.bibliocommons.com/v2/holds'

with open("joco_auth.txt") as f:
	name = str(f.readline()).strip()
	pin = str(f.read()).strip()

payload = {
    'name': name,
	'user_pin': pin  #Preferably set your password in an env variable and sub it in.
}

def get_holds():
	with requests.Session() as session:
		post = session.post(POST_LOGIN_URL, data=payload)
		r = session.get(REQUEST_URL)
		soup = BeautifulSoup(r.text, 'html.parser')

	list_section = soup.find(class_='cp-holds-list')
	list_elements = list_section.find_all(class_='cp-batch-actions-list-item')
	titles = {i.find(class_='title-content').string: i.find(class_='status-name').string for i in list_elements}
	return titles

print(get_holds())