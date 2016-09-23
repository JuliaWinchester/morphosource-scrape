'''
Created on Sep 19, 2016

This script automates batch downloads of PLY media from www.morphosource.org. It
requires a separate user.py module placed in the same directory as scrape.py. 
The user.py module should define variables 'username' and 'password' for 
MorphoSource access. Specimens are identified by specimen number and only PLY
media titled 'Raw/Surface Cropped' are downloaded, but with some customization
the basic protocol of this script can serve as a guide for other situations 
requiring batch media downloads from MorphoSource. 

@author: Julie Winchester
'''
import requests
import os
import csv
import user

def find_download(id, session_requests):
	response = session_requests.get(query_url+str(id))
	response_json = response.json()
	for result in response_json['results']:
		for media in result['medium.media']:
			if media['title'] == 'Raw Surface/Cropped':
				return media['download']
	return False

# Getting specimen numbers
with open('C:\Code\morphosource-scrape\specimen_numbers.csv', 'r') as csvfile:
	reader = csv.reader(csvfile)
	full_list = list(reader)
	flat_list = [item for sublist in full_list[1:] for item in sublist]
	specimen_numbers = [''.join(filter(str.isdigit, x)) for x in flat_list]
# Alternately...
# specimen_numbers = [171063, 284782, 290601, 211460, 211465]

save_dir = 'C:/Code/morphosource-scrape/files'
session_requests = requests.session()

# Scraping
query_url = 'http://www.morphosource.org/api/v1/find/media?q=specimen.catalog_number:'

specimen_links = []
specimen_ids_no_downloads = []

print('Beginning scraping for download links')

for id in specimen_numbers:
	print('Scraping for specimen ID ' + str(id))
	download = find_download(id, session_requests)
	if download == False:
		specimen_ids_no_downloads.append(id)
		print("No 'Raw Surface/Cropped' link found for specimen ID " + str(id))
	else:
		specimen_links.append({'id': id, 'download': download})
		print("'Raw Surface/Cropped' link found for specimen ID " + str(id))

print('Finished scraping for download links\nFound ' + str(len(specimen_links)) + ' links.')

if len(specimen_ids_no_downloads) > 0:
	print('Download links were not found for the following specimens')
	print(specimen_ids_no_downloads )

# Logging in
login_url = 'http://www.morphosource.org/LoginReg/login'
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
data = 'username=' + user.username +'&password=' + user.password

login_result = session_requests.post(login_url, headers = headers, data = data)

# Downloading files
for specimen in specimen_links:
	print('Downloading file for specimen ID ' + str(specimen['id']))
	file_result = session_requests.get(specimen['download'])
	file = open(os.path.join(save_dir, str(specimen['id'])+'.zip'), 'wb')
	file.write(file_result.content)
	file.close()

print('File downloads finished')
