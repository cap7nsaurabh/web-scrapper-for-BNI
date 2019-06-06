#----------------------------------------------------------------------------------------
#these variables are to changed according to use case. Please refer to readme.txt
excel_file_path=r"copy path to your excel file here attaching filename (.xls) example: c:\data.xls"
resume_variable=0 #change in case of script failure due to slow internet
webdriver_path=r"copy path of chrome webdriver exectutable file here attaching file name in the end (.exe) example: c:\chromedriver.exe (please refer readme.txt)"
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#make sure you have these libraries installed before running the script (please refer readme.txt)
import requests
from xlwt import Workbook
from xlutils.copy import copy
import xlrd
try:
    from bs4 import BeautifulSoup
except:
    print("install bs4 using pip install bs4")
try:
    from selenium import webdriver
except:
    print("install latest version of selenium using pip")
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
#fetching BNI-GURGAON data
headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
url="https://bni-india.in/find-a-chapter/"
try:
    request=requests.get(url,headers=headers).text
except requests.exceptions.RequestException as e:  # handles requests error
    print (e)
#getting data for "bni gurgaon"
page=BeautifulSoup(request,'html.parser')
container=page.find(class_="vc_column-inner vc_custom_1486453680500")
bniname=container.h5.get_text()
bnicontact=container.p.strong.next_sibling.next_sibling
bni_mail_id=container.p.a.get_text()
bni_phone='+'+container.p.get_text().split('+')[1].split('\n')[0]
dict=[{}]
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
#setting up selenium browsers to parse dynamic content (not possible using BeautifulSoup)
path = webdriver_path
try:
    browser = webdriver.Chrome(path)
except:
    print("download the webdriver from chrome using link: http://chromedriver.chromium.org/downloads")
    print("install the same version as the version of chrome you are using.")
    print("set path variable (declared above as path of your chromewebdriver that you downloaded)")
member_list_page_url="http://bni-gurgaon.in/en-IN/memberlist?chapterName=&chapterCity=&chapterArea=&memberFirstName=&memberKeywords=&memberLastName=&memberCompany=&regionIds=3906"
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
#setting up excel sheet
rb = xlrd.open_workbook(excel_file_path)
wb=copy(rb)
sheet=wb.get_sheet(0)
sheet.write(0,0,"S no")
sheet.write(0,1,"BNI NAME")
sheet.write(0,2,"BNI Contact")
sheet.write(0,3,"BNI_phone")
sheet.write(0,4,"BNI_email")
sheet.write(0,5,"Member_name")
sheet.write(0,6,"Member_Region")
sheet.write(0,7,"Member_city")
sheet.write(0,8,"Member_Area")
sheet.write(0,9,"Member_profession")
sheet.write(0,10,"Member_company")
sheet.write(0,11,"Member_phone")
sheet.write(0,12,"Member_mobile")
sheet.write(0,13,"Member_website")
sheet.write(0,14,"Member_address")
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
#function to get individual members detailed data
def get_individual_member(page_url):
    browser1 = webdriver.Chrome(path)
    browser1.get(page_url)
    dict2={}
    t=0
    listp=[]
    listad=[]
    stre=""
    st=""
    te=[]
    listp = browser1.find_elements_by_xpath("//*[@id='memberDetail']/section/div/div[1]/div[2]")
    if len(listp)!=0:
        te=listp[0].text.split('\n')
        te=te[1:len(te):2]
    if len(te)==0 or len(listp)==0:
        dict2["phone"]="na"
        dict2["mobile"]="na"
        dict2["website"]="na"
    elif len(te)==1:
        dict2["phone"]=te[0]
        dict2["mobile"]="na"
        dict2["website"]="na"
    elif len(te)==2:
        dict2["phone"] = te[0]
        dict2["mobile"]="na"
        dict2["website"] = te[1]
    elif len(te)==3:
        dict2["phone"] = te[0]
        dict2["mobile"]=te[1]
        dict2["website"] = te[2]
    elif len(te)==4:
        dict2["phone"] = te[0]
        dict2["mobile"]=te[1]
        dict2["website"] = te[3]
    elif len(te) > 4:
        dict2["phone"] = te[0]
        dict2["mobile"] = te[1]
        dict2["website"] = te[len(te)-1]
    listad=browser1.find_element_by_xpath("//*[@id='memberDetail']/section/div/div[1]/div[3]")
    stre=listad.find_elements_by_tag_name('p')
    if len(stre)>1:
        st=stre[1].text[1:].split('\n')[1:]
    else:
        st = stre[0].text[1:].split('\n')[1:]
    address=""
    for ite in st:
        address=address+"\n"+ite
    dict2["address"]=address
    browser1.close()
    return dict2
#returns a list with data
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
#function to get members list in a BNI.
def get_members(url_for_member_list,dict,sheet1):
    try:
        req=browser.get(url_for_member_list)
    except:
        print("make sure you are connected to internet  and have setup the chrome webdriver properly")
    list=browser.find_elements_by_xpath("//tr[@role='row']")
    print("total {} records found".format(len(list)))
    i=resume_variable
    for item in list[resume_variable:len(list)-1]:
        print("getting data for record : {}".format(i))
        i=i+1
        memdata = {}
        list2=item.find_elements_by_tag_name('td')
        taga=item.find_element_by_tag_name('a')
        url2=taga.get_attribute('href')
        indi=get_individual_member(url2)
        memdata['mem_name']=list2[0].text
        memdata['mem_region']=list2[1].text
        memdata['mem_city']=list2[2].text
        memdata['mem_area']=list2[3].text
        memdata['mem_profession']=list2[4].text
        memdata['mem_company']=list2[5].text
        memdata['phone']=indi['phone']
        memdata['mobile']=indi['mobile']
        memdata['website']=indi['website']
        memdata['address']=indi['address']
        memdata['bni_name']=bniname
        memdata['bni_contact']=bnicontact
        memdata["bni_phone"]=bni_phone
        memdata["bni_email"]=bni_mail_id
        sheet.write(0 + i + 1, 0, str(i))
        sheet.write(0+i+1, 1, memdata['bni_name'])
        sheet.write(0+i+1, 2, memdata['bni_contact'])
        sheet.write(0+i+1, 3, memdata["bni_phone"])
        sheet.write(0+i+1, 4, memdata["bni_email"])
        sheet.write(0+i+1, 5, memdata['mem_name'])
        sheet.write(0+i+1, 6, memdata['mem_region'])
        sheet.write(0+i+1, 7, memdata['mem_city'])
        sheet.write(0+i+1, 8, memdata['mem_area'])
        sheet.write(0+i+1, 9, memdata['mem_profession'])
        sheet.write(0+i+1, 10,memdata['mem_company'])
        sheet.write(0+i+1, 11,memdata['phone'])
        sheet.write(0+i+1, 12,memdata['mobile'])
        sheet.write(0+i+1, 13,memdata['website'])
        sheet.write(0+i+1, 14,memdata['address'])
        wb.save(excel_file_path)
        dict.append(memdata)
    return dict
#also writes to the excel sheet along with parsing. returns a list of dictionaries with required data
#--------------------------------------------------------------------------------------------------------------------
urlmemlist="http://bni-gurgaon.in/en-IN/memberlist?chapterName=&chapterCity=&chapterArea=&memberFirstName=&memberKeywords=&memberLastName=&memberCompany=&regionIds=3906"
get_members(urlmemlist,dict,sheet)
print(dict)