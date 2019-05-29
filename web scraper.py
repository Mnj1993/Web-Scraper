""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"   WEB SCRAPER                                                                                                    "
"The program  extracts the basic data about the top cities in United States based on the population of each cities."
"and collects the basic informations each cities such as County,year of Settled,Incorporated,Government Type,Mayor,"
"City, Land Area, Area covered by Water,Elevation,Time zone, Time zone at Summer,Website,ZIP Codes,Area codes,     "
"population Density.                                                                                               "
"the output is stored as  Top_cities_in_the_United_States.csv , that is compatible to store as BigQuery table.     "
"The program was developed in Anaconda spyder and python 3.6                                                       "
"                                                                                                                  "
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""
@author: manoj007

"""
import requests
from bs4 import BeautifulSoup
import csv
import codecs
import pandas as pd


##################################################
#         function to based table thread         #
##################################################
def Row_data(My_table,soup):
    list_of_rows = []
    for row in My_table.findAll('tr'):
        list_of_cells = []
        for cell in row.findAll(["th","td"]):
            text = cell.text
            list_of_cells.append(text)
        list_of_rows.append(list_of_cells)
    temp=data_format(list_of_rows)
    temp1 = sub_data(soup)
    return(merge_data(temp,temp1))
    
##################################################
#     function to format the base data           #
##################################################
def commas(word):
    word=str(word)
    if "," not in word:
        words=word.replace('\n',',')
        words=sqkm(words)
        return(words)
    else:
        
        words=word.replace(',',"")
        words=words.replace('\n',',')
        words=sqkm(words)
        return(words)
        
def sqkm(word):
    if "sq" in word:
        return(word.replace("mi,","mi;"))
        print(word)
    elif "/sq" in word:
        return(word.replace("/sq mi,","/sq mi;"))
        print(word)
    else:
        return(word)

##################################################
#       funtion to collect the based data        #
##################################################            
def data_format(list_of_rows):
    dataform=list()
    for i in range(0,len(list_of_rows)):
        #k=[]
        str1=""
        for j in range(0,len(list_of_rows[i])):
            str1=str1+commas(list_of_rows[i][j])
        str1=str1[:-1]
        dataform.append([str1])
    return(dataform)


##################################################
# opening the the city reference from base table #
##################################################
def sub_data(soup):
    tb = soup.find_all('table')[4]
    dff = pd.read_html(str(tb),encoding='utf-8', header=0)[0]
    dff=(dff.iloc[:,1])
    data = [[td.a['href'] if td.find('a') else ''.join(td.stripped_strings) for td in row.find_all('td')] for row in tb.find_all('tr')]
    return(href_list(data))
    
##################################################
# collecting the city reference from base table  #
################################################## 
def href_list(data):
    list_of_href=[]
    for i in range(0,len(data)-1):
        list_of_href.append(url[0:24]+data[1:][i][1])
    return(city_details(list_of_href))

#####################################################################
#    crawling the city website to gather the basic information      #
##################################################################### 
def city_details(list_of_href):
    extra=[]
    name=['County','Settled','Incorporated','• Type','• Mayor','• City','• Land','• Water',
          'Elevation','Time zone','• Summer (DST)','Website','ZIP Codes','Area codes','• Density']
    extra=[["wiki_link,"+",".join(name)]]
    for i in range(0,len(list_of_href)):
        r = requests.get(list_of_href[i])
        soup = BeautifulSoup(r.text, 'lxml')
        tb = soup.find_all('table')[0]
        dd = pd.read_html(str(tb),encoding='utf-8', header=0)[0]
        extra1=[]
        s=''
        #print("3k")
        extra1.append(list_of_href[i])
        for o in range(0,len(name)):
            extra1.append([x[1] for x in dd.values if name[o] in x])
            s=[("".join(h)).replace(',','') for h in extra1]
        extra.append(s)
        if (i%5 == 0):print("=",end="", flush=True) 
    print(" ")
    print("completed...")
    return(extra)

##################################################
#    merging the sub_data to the base table      #
################################################## 
def merge_data(d,extra):
    final=[]
    for i in range(0,len(d)):
        final.append(d[i]+extra[i])
    return(final)


##################################################
#        function to copy the data               #
################################################## 
def write_data(final):
    data=[]
    for data in final:
        writer.writerow(data)


if __name__ == "__main__":
    #################################################
    #             open a empty .csv                 #
    #################################################
    outfile = codecs.open("Top_cities_in_the_United_States.csv","w",encoding='ascii', errors='ignore')
    writer = csv.writer(outfile,quotechar=' ')

    ##################################################
    # opening the website and tracking the base table#
    ##################################################    
    url='https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population'
    r = requests.get('https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population')
    soup = BeautifulSoup(r.text, 'lxml')
    My_table = soup.find('table',{'class':'wikitable sortable'})
    
    ##################################################
    #        crawling to gathering the data          #
    ################################################## 
    
    print("Data processing....\n")
    data_formt=Row_data(My_table,soup)
    
    ##################################################
    #        copying the data to the .csv file       #
    ################################################## 
    write_data(data_formt)
    outfile.close()