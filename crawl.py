import urllib2
from bs4 import BeautifulSoup
import csv
import time

## define interval of issue IDs to scrape
issueid_start = 41334
issueid_end = 160700

## path to store issues
issues_path = '/path_to_dir/'
## path to store comments
comments_path = '/path_to_dir/'

for issue_id in range(issueid_start,issueid_end):

	## sleep for 1 second to be "nice" to the issue tracker
	time.sleep(1)

	try:

		## open issue from the tracker --
		page = urllib2.urlopen('https://code.google.com/p/android/issues/detail?id=' + str(issue_id)).read()

		## create soup
		soup = BeautifulSoup(page,from_encoding='utf-8')
		soup.prettify()

		#### heading of the issue
		issue = soup.find('span', {"class" : "h3"})

		if issue:
			issue_heading = soup.find('span', {"class" : "h3"}).contents[0]

			############# SCRAPE ISSUE META ##################
			#### status of issue
			issue_meta = soup.find('td', {"id" : "issuemeta"})
			issue_meta_td = issue_meta.findAll('td')

			count=0
			## list to contain meta content
			list_meta = []

			for column in issue_meta_td:

				if count==0:
					span = column.find('span')
					if span:
						list_meta.append(span.contents[0])
					else:
						list_meta.append('NA')

				elif count==3:
					a = column.find('a')
					if a:
						if(len(a.contents)==2):
							list_meta.append(a.contents[1])
						else:
							list_meta.append('NA')
					else:
						list_meta.append('NA')

				else:
					a = column.find('a')
					if a:
						if(len(a.contents)==2):
							list_meta.append(a.contents[1])
						else:
							list_meta.append(a.contents[0])
					else:
						list_meta.append('NA')

				count +=1


			############ SCRAEP ISSUE DESCRIPTION #############
			issue_description = soup.find('div',{'class':'cursor_off vt issuedescription'})
			issue_description_authors = issue_description.find('div',{'class':'author'})
			issue_loggedBy = 'NA'
			issue_loggedAt = 'NA'

			if issue_description_authors.a and issue_description_authors.a.has_attr('href'):
				issue_loggedBy = issue_description_authors.a['href']

			if issue_description_authors.span and issue_description_authors.span.has_attr('title'):
				issue_loggedAt = issue_description_authors.span['title']

			## write issue description to file
			issue_description_content = issue_description.pre.contents  ## should save this to file
			f = open(issues_path+str(issue_id),'w')

			for lines in issue_description_content:
				f.write(lines.encode('utf-8'))
			
			f.close()


			## list to contain comment times 
			list_times = []

			## list of comment IDs -- reference to comment file names
			list_commentIDs = []

			############ SCRAPE ISSUE COMMENTS ################
			issue_comments = soup.findAll('div',{'class':'cursor_off vt issuecomment'})

			for comment in issue_comments:
				#print(comment)
				#time = comment.find('span',{'class':'date'})
				#print((comment.find('span',{'class':'date'})).contents)
				list_times.append(comment.find('span',{'class':'date'})['title']) ## comment logged at
				comment_id = str(issue_id) + '_'+ comment['id']
				list_commentIDs.append(comment_id) ## comment ID
				content = comment.pre.contents

				## write comments to file
				f = open(comments_path+comment_id,'w')

				for lines in content:
					f.write(lines.encode('utf-8'))
				

				f.close()
				#print(content)


			with open(issues_path+'issues.csv', 'a') as fp:
				a = csv.writer(fp, delimiter=',')
				#print(list_meta)
				#print(','.join(list_meta))
				if len(list_meta)==4:
					data = [issue_id,issue_heading.encode('utf-8'),list_meta[0].encode('utf-8'),list_meta[1].encode('utf-8'),list_meta[2].encode('utf-8'),list_meta[3].encode('utf-8'),issue_loggedBy,issue_loggedAt,';'.join(list_times).encode('utf-8'),";".join(list_commentIDs).encode('utf-8')]
				else:
					data = [issue_id,issue_heading.encode('utf-8'),list_meta[0].encode('utf-8'),list_meta[1].encode('utf-8'),'',list_meta[2].encode('utf-8'),issue_loggedBy,issue_loggedAt,';'.join(list_times).encode('utf-8'),";".join(list_commentIDs).encode('utf-8')]
				

				#print(data)
				a.writerow(data)


	except urllib2.HTTPError, e:
	    print 'We failed with error code - %s.' % e.code 

	except urllib2.URLError, err:
		print "Some other error happened:", err.reason

