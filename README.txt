
The folder contains two scripts (main.py and wiki_crawler.py), two html files for documentation,a text file with the question's answers and two text files with sample results. 

- Main.py executes the crawling and returns percentage of pages that make it the Philosophy page and distribution of path lengths.	wiki_crawler.py contains all the functions needed to crawl wikipedia.

- HTML files contain the documentation for main.py and wiki_crawler.py


-  results.txt contain the percentage of pages that lead to philosophy and the number of pages each random page went through. This was done on 100 random pages

- distribution_file.txt contains  the distribution for path lengths that made it to the Philosophy page. This was executed on 500 random pages that end up to the Philosophy page.

Library used:
	- json
	- sys
	- time 
	- bs4 (BeautifulSoup)
	- requests
	- re



