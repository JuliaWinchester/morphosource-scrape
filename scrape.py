import requests
import user
from lxml import html

def find_download(id, session_requests):
	response = session_requests.get(query_url+str(id))
	response_json = response.json()
	for result in response_json['results']:
		for media in result['medium.media']:
			if media['title'] == 'Raw Surface/Cropped':
				return media['download']
	return False

specimen_numbers = [171063, 284782, 290601, 211460, 211465]
save_dir = 'savedir'

session_requests = requests.session()

# Scraping

query_url = 'http://www.morphosource.org/api/v1/find/media?q=specimen.catalog_number:'

specimen_links = []
specimen_ids_no_downloads = []

print 'Beginning scraping for download links'

for id in specimen_numbers:
	print 'Scraping for specimen ID ' + str(id)
	download = find_download(id, session_requests)
	if download == False:
		specimen_ids_no_downloads.append(id)
		print "No 'Raw Surface/Cropped' link found for specimen ID " + str(id)
	else:
		specimen_links.append({'id': id, 'download': download})
		print "'Raw Surface/Cropped' link found for specimen ID " + str(id)

print 'Finished scraping for download links\nFound ' + str(len(specimen_links)) + ' links.'

if len(specimen_ids_no_downloads) > 0:
	print 'Download links were not found for the following specimens'
	print specimen_ids_no_downloads 

# Logging in
login_url = 'http://www.morphosource.org/LoginReg/login'
headers = {'Origin': 'http://www.morphosource.org', 
		   'Referer': 'http://www.morphosource.org/LoginReg/form'}
data = 'username=' + user.username +'&password=' + user.password

login_result = session_requests.post(login_url, headers = headers, data = data)



