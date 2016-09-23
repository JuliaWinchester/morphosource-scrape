# morphosource-scrape

This script automates batch downloads of media files from [MorphoSource](http://www.morphosource.org). A separate user.py module should be placed in the same directory as scrape.py, and this module should define the variables 'username' and 'password' for MorphoSource access. Specimens are identified by specimen number and only surface mesh media titled 'Raw/Surface Cropped' are downloaded, but the basic protocol of this script can be used as a guide for other situations requiring batch media downloads from MorphoSource.
