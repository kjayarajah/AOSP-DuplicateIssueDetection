import urllib2, os
from bs4 import BeautifulSoup
import csv
import time


#name of directory to store data to
path = '/path_to_dir/'
#CSV file to contain meta data of packages
metafile = '/packages.csv'
	

try:

	## Package listing page
	page = urllib2.urlopen('http://developer.android.com/reference/packages.html').read()

	## create soup
	soup = BeautifulSoup(page,from_encoding='utf-8')
	soup.prettify()

	## fetch path to every package summary page
	table = soup.find('table',{'class':'jd-sumtable'})
	tr = table.findAll('tr')

	for row in tr:

		## name and link of package
		pkgname = row.find('td',{'class':'jd-linkcol'}).a.contents
		pkglink = row.find('td',{'class':'jd-linkcol'}).a['href']

		## description of pkg
		description = ['NA']
		desc_soup = row.find('td',{'class':'jd-descrcol'}).p
		if desc_soup:
			description = desc_soup.contents

		
		## go to package link
		package = urllib2.urlopen('http://developer.android.com' + pkglink).read()

		## create soup
		pkg_soup = BeautifulSoup(package,from_encoding='utf-8')
		pkg_soup.prettify()

		## get package description in full
		print(pkgname)
		full_description = pkg_soup.find('div',{'class':'jd-descr'})


		### list of classes/interfaces/annotations/anything it is linked to
		classes = pkg_soup.findAll('table', {'class':'jd-sumtable-expando'})

		for class_table in classes:

			## get list of classes
			class_list = class_table.findAll('tr')


			## for each row -- get name, link and description
			for cl in class_list:
				a = cl.find('td',{'class':'jd-linkcol'}).a
				name = 'NA'
				lin = 'NA'

				if a:
					name = a.contents[0]
					link = cl.find('td',{'class':'jd-linkcol'}).a['href']

				else:
					name = cl.find('td',{'class':'jd-linkcol'}).contents[0]

				
				## short description
				c_description = ['NA']
				c_soup = cl.find('td',{'class':'jd-descrcol'}).p

				if c_soup:
					c_description = c_soup.contents

				## write entries to file
				with open(metafile, 'a') as fp:
					a = csv.writer(fp, delimiter=',')

					data = [pkgname[0].encode('utf-8'),pkglink,name.encode('utf-8'),link]
					a.writerow(data)


		## write full package description to file
		dir = os.path.dirname(path+pkglink)	## check if path exists -- if not create
		if not os.path.exists(dir):
			os.makedirs(dir)

		if full_description:
			f = open(path+pkglink,'w')

			for lines in full_description.contents:
				f.write(lines.encode('utf-8'))

			f.close()		






	

except urllib2.HTTPError, e:
    print 'We failed with error code - %s.' % e.code 

