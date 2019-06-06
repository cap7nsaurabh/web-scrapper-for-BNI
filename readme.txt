SAURABH SINGH PYTHON TEST

#run the script using any python IDLE 
*(not suitable for runnig through commandline)*
#library requirements to run the scripts
	1.requests
	2.bs4
	3.xlrd
	4.xlwt
	5.xlutils
	6.selenium

**the scripts uses chrome webdriver to parse dynamic content. please download the version 
  of chrome wedriver (same as version of chrome running in your system).
  get webdriver at :http://chromedriver.chromium.org/downloads and selecting your version 
  (if you don't have chrome browser 
   get at :https://www.google.com/chrome/?brand=CHBD&gclid=Cj0KEQjw8-LnBRCyxtfMl-Cbu48BEiQA6eUMGn5yfi3xnePwrKYhwjnhqzmGG7uujgbhMRrwl69qUGIaAsmS8P8HAQ&gclsrc=aw.ds)  
#USE CASE:
	1: Please don't forget to set path to chrome webdriver in the script by copying value to webdriver_path 
	2: Please don't forget to set path to excel file in the script by copying value to excel_file_path variable
	3: the script prints the record it is parsing. The scripts tends to crash in case of slow internet or selenium crashing so
		there is need to worry. Just change the value of resume variable to the last record no: and rerun the script so it appends the data to existing 
		excel file.