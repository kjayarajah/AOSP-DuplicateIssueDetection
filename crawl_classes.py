import urllib2, os
from bs4 import BeautifulSoup
import csv
import time

#name of directory to store data to
path = '/path_to_dir/'

try:

	## Package listing page
	page = urllib2.urlopen('http://developer.android.com/reference/classes.html').read()

	## create soup
	soup = BeautifulSoup(page,from_encoding='utf-8')
	soup.prettify()

	## fetch path to every package summary page
	table = soup.findAll('table',{'class':'jd-sumtable'})

	for tb in table:
		tr = tb.findAll('tr')

		for row in tr:

			clsname = row.find('td',{'class':'jd-linkcol'}).a.contents

			print(clsname)

			clslink = row.find('td',{'class':'jd-linkcol'}).a['href']
			
			## go to class link
			package = urllib2.urlopen('http://developer.android.com' + clslink).read()

			## create soup
			pkg_soup = BeautifulSoup(package,from_encoding='utf-8')
			pkg_soup.prettify()

			## find all p and a
			all_p = pkg_soup.findAll('p')

			dir = os.path.dirname(path+clslink)	## check if path exists -- if not create
			if not os.path.exists(dir):
				os.makedirs(dir)

			f = open(path+clslink, 'a')

			for p in all_p:
				if hasattr(p.contents, '__iter__'):
					for c in p.contents:
						f.write(c.encode('utf-8'))
				else:
					f.write(p.contents.encode('utf-8'))

			## find all a
			all_a = pkg_soup.findAll('span',{'class':'sympad'})

			for a in all_a:
				#print (a.a)
				if a.a:
					f.write(a.a.contents[0].encode('utf-8'))

			## find all summary description
			all_div = pkg_soup.findAll('div',{'class':'jd-descrdiv'})

			for d in all_div:
				if hasattr(d.contents, '__iter__'):
					for c in d.contents:
						f.write(c.encode('utf-8'))
				else:
					f.write(d.contents.encode('utf-8'))


			f.close()


		

except urllib2.HTTPError, e:
    print 'We failed with error code - %s.' % e.code 
