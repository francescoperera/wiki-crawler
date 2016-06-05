"""
this script executes the crawling and calculates the percentage of pages that made it to the Philosophy page and the distribution of all path lenghts 
"""

import wiki_crawler
import json
import sys
import time 

paths_dict={}


def save_crawling_to_file(d,f):
	"""
	save_crawling_to_file takes some data d and a file f as input and saves d into f.
	"""
	with open(f, 'w') as outfile:
		json.dump(d, outfile)

def crawl(url,i,f):
	"""
	crawl takes a url and crawls until it gets to Philosophy or it gets stuck in loop. 
	The function crawls i(integer) different Wikipedia pages. The function returns a dictionary with the total crawling history for all i pages
	and the number of  atempts that either reached or not the Philosophy page. All outputs are saved to file f
	"""
	global paths_dict
	global requests_count
	crawling_history={} #  contains the counts needed to get to Philosophy for each succesful/valid attempt
	pages_visited ={} # contains the counts from all attempts both succesful and unsuccesful 
	counter = 1
	to_philosophy = 0
	not_to_philosophy=0

	while to_philosophy < i:
		print "Attempt " + str(counter)
		crawl_count= wiki_crawler.crawl_to_philosophy(url,paths_dict)
		if crawl_count!= None :
			if crawl_count ==  -1:
				not_to_philosophy +=1
			else:
				to_philosophy +=1
				crawling_history[str(to_philosophy)] = crawl_count
			pages_visited[str(counter)] = crawl_count
		else:
			not_to_philosophy +=1
		counter +=1

	save_crawling_to_file(pages_visited,f)
	return crawling_history,to_philosophy,not_to_philosophy


def percentage(x,y):
	"""
	the function takes integers calculates the percentage for x
	"""
	percentage = (float(x)/float(x+y)) * 100
	return percentage

def path_length_distribution(crawling_history,f):
	"""
	path_length_distribution takes the crawling history dictionary and uses to create a new dictionary with the distribution of each path length.
	The function also returns the most_frequent_path_length. Both outputs are saved to file f
	"""
	distribution = {}
	distribution_to_file ={}

	path_length = sorted([crawling_history[x] for x in crawling_history.keys()])
	for i in range(len(path_length)):
		if str(path_length[i]) in distribution.keys():
			distribution[str(path_length[i])] += 1
		else:
			distribution[str(path_length[i])] = 1

	most_frequent_path_length = max(distribution, key=lambda i: distribution[i])
	distribution_to_file["most_frequent_path_length"] = most_frequent_path_length
	distribution_to_file["distribution"] = distribution

	save_crawling_to_file(distribution_to_file,f)

	return distribution,most_frequent_path_length

if __name__ == '__main__':
	start_time = time.time()
	random_url = 'http://en.wikipedia.org/wiki/Special:Random'

	if len(sys.argv)==1:
		# if no arguments, use random Wikipedia page
		start_url = random_url
	else:
		start_url = sys.argv[1]

	results_file = "results_file.txt"
	distribution_file = "new_distribution_file.txt"
	crawling_hist,num_to_phil,num_not_to_phil = crawl(start_url,100,results_file)
	crawl_time = time.time() - start_time
	print "Crawling took " + str(crawl_time) + " seconds"

	distribution,most_frequent_path_length = path_length_distribution(crawling_hist,distribution_file)
	print "The distribution of all path lengths is:"
	print distribution
	print "the most frequent path length is "+str(most_frequent_path_length)

	percent = percentage(num_to_phil,num_not_to_phil)
	print "The percentage of wikipedia pages that lead to the Philosophy page is: " + str(percent)
	

  







