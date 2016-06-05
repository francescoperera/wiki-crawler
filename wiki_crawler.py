"""
this script contains all the function required to crawl wikipedia 
"""

import sys
import requests
from requests.exceptions import ConnectionError
import re
from bs4 import BeautifulSoup
import time

stop_url= 'http://en.wikipedia.org/wiki/Philosophy' 
requests_count = 0

def send_requests(url):
	"""
	send_requests takes an url and sends a get request. The received response object is
	then turned into a BeautifulSoup object
	"""
	response = requests.get(url)
	soup = BeautifulSoup(response.text)
	return soup

def clean_paragraph(p):
	"""
	clean_paragraph takes a p(an html paragraph) and replaces span tags (which contain italicized links) with empty strings. 
	The function also replaces the text and tags enclosed by parenthesis with empty strings.
	The function returns the cleaned/corrected paragraph named corrected_p
	"""

	if p.find_all("span") == None:
		p_text = p
	else:
		for span_tag in p.find_all("span"):
			span_tag.replace_with("")
		p_text = str(p)
	corrected_p = re.sub(r' \(.*?\)', "", p_text)
	return corrected_p

def get_next_page_link(url):
	"""
	get_next_page_link takes an url as input and parses the html to find the next valid link.
	If a next valid link is found, the function returns next_link. However, if no valid link
	is found, the function returns a dummy value of -1.
	"""
	while True:
		try:
				soup = send_requests(url)
				break
		except ConnectionError:
				time.sleep(1)
				soup = send_requests(url)

	print(soup.title.get_text()) # print the title of the current wikipedia page
	content = soup.find(id='mw-content-text')

	if content == None:
			# the wikipedia page might not have a main of text, so no valid link is present.
			return -1

	if len(soup.select('div#mw-content-text > p')) == 0:
			# the wikipedia page has no paragraphs, so no valid link is present
			return -1

	else:
			if len(soup.select('div#mw-content-text > p > a')) == 0:
				# if no hyperlink is present in the paragraphs, then check for hyperlinks in lists. It is assumed that lists are not considered main body of text
				return -1
				# if len(soup.select('div#mw-content-text > ul > li > a')) !=0:
				# 	next_link = soup.select('div#mw-content-text > ul > li > a')[0]
				# else:
				# 	# if no  hyperlinks in paragraphs or lists were found then no valid link is present
				# 	return -1

			else:
					# the wikipedia page has paragraphs and a hyperlink might be present
					paragraph = soup.select('div#mw-content-text > p')[0] # paragraph is the first paragraph in the body of the page
					while paragraph == None:
						paragraph = paragraph.find_next_sibling("p")
					paragraph_text = clean_paragraph(paragraph)
					corrected_paragraph = BeautifulSoup(paragraph_text)
					next_link = corrected_paragraph.find(href = re.compile("/wiki/")) # next_link is the first link in the paragraph. The link is neither italicized or in parenthesis

					if next_link != None and "//en.wiktionary.org/" in next_link.get('href'):
						# this handles the case that next_link captured a wiktionary link. Find the next available wikipedia link instead
						next_link = next_link.find_next('a')

					if next_link != None and "note" in next_link.get('href'): 
						# this replace hyperlinks that lead to other sections of the same page
						next_link = next_link.find_next('a')

					while next_link == None: 
					# next_link might be None because the paragraph does not have a valid link
						if '(disambiguation)' in url: 
							# case 1 = the first link the function found is one that contains '(disambiguation)' and it leads to a similar wikipedia page
							next_link = content.ul.find(href = re.compile("/wiki/"))
						else:
							# case 2 = the first paragraph did not contain any valid links. Look at the next paragraphs for valid links
							paragraph = paragraph.find_next_sibling("p")
							if paragraph == None:
								# if there are no more paragraphs, then no valid links are present in the page
								return -1
							paragraph_text = clean_paragraph(paragraph)
							corrected_paragraph = BeautifulSoup(paragraph_text)
							next_link = corrected_paragraph.find(href = re.compile("/wiki/"))

			if "//en.wikipedia.org/" in next_link.get('href'): 
				# some of the hrefs have "//en.wikipedia.org/" in it, set the url differently for these hrefs
				url = 'http:'+ next_link.get('href')
			else:
				# most hrefs only have /wiki/Page_Title , set url accordingly
				url = 'http://en.wikipedia.org' + next_link.get('href')

	return url

def crawl_to_philosophy(url,paths_dict):
	"""
	crawl_to_philosophy takes an url and a dictionary called paths. It crawls through wikipedia pages until it reaches the Philosophy page 
	or until it gets stuck in a loop and it returns a dummy variable -1.
	The function returns the number of wikipedia pages it clicked through to get the to the Philosophy page or -1 if it did not get to that page.
	"""
	global stop_title
	global requests_count
	
	count = 0
	paths_at_attempt =set()

	current = get_next_page_link(url)
	requests_count +=1

	if current == -1:
		return count

	while stop_url!= current:
		if current in paths_at_attempt:
			# the crawler went back to a page that it just visited. This is a sign that the crawler is stuck in a loop
			return -1
		paths_at_attempt.add(current)

		# if the link of the current page is the paths dictionary, then instead of sending requests to the wikipedia server,the function traversals the dictionary to get to Philosophy
		if current in paths_dict.keys():
			next = paths_dict[current]
		else:
			next= get_next_page_link(current)
			requests_count+=1
			if next == -1:
				return -1
			paths_dict[current] = next
				
		current = next
		count = count+1

	if next == stop_url:
	  print next.split('/')[-1] + " - Wikipedia, the free encyclopedia"
	  print "At this point a total of "+ str(requests_count) + " requests were made"

	return count

if __name__ == '__main__':
	url_starting = 'https://en.wikipedia.org/wiki/Special:Random'
	wiki_count = crawl_to_philosophy(url_starting)
	print(str(wiki_count) + " wikipedia pages were visited ")
