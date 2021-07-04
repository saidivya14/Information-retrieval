IR_Project
==============================

Zip files has the following files: 
1. crawler.py - Crawler code
2. FileDownload.py 
3. Crawled Urls.txt - list of urls 
4. invertedindex.py - inverted index,search,ranking code
5. postlinglist.txt
6. README.txt - read me
7. Downloaded_Files folder - dataset folder 

1. Instruction for compiling and running
   - Zip file comes with crawler.py python 3 file, which has the crawler code in python
   - Already seed url is present in crawler.py code,so when we run the code it creates Crawled Urls.txt-list of urls
   - We call FileDownload.py in crawler.py so it forms Downloaded_files folder ==> dataset
     Run the program to crawl and scrap urls: 
          python crawler.py
   - Invertedindex.py file created inverted index for dictionary and save posting lists in postinglist.txt
   - It ranks the documents relevant to the query and retrieves top 10 
   	  Run the program to retrieve top 10 relevant docs:
   		  python invertedindex.py

