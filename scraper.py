from bs4 import BeautifulSoup
import requests
import pandas as pd 
from itertools import zip_longest
import csv


#requesting and parsing the link 
result = requests.get('https://biztimes.com/nonprofit-directory/').content
soup = BeautifulSoup(result,"lxml")

company = soup.find_all("h4", {"class":"directory-listing-title"})

#Find the data of each company
data = soup.find_all("dl")

rows = {"Company:": [], "Address:": [], "Phone:": [], "Website:":[], "Year founded:": [], "Facebook:" :[], "Twitter:" :[]}
heads = list(rows.keys())[1:-1]

# Exploring the data of each company
for i in range(len(data)):
    #titles of the data
    header = data[i].find_all("dt")
    #the content of the headers
    content = data[i].find_all("dd")
    
    rows['Company:'].append(company[i].text)
    # to validate the existing of each type of data
    vali = {"Address:": False, "Phone:": False, "Website:": False, "Year founded:": False, "Facebook:": False, "Twitter:": False}
    for i in range(len(header)):
        if header[i].text == list(vali.keys())[i]:
            vali[header[i].text] = True
            
    #adding data to rows dictionary
    for i in range(len(heads)):
        
        if vali[heads[i]] == True:
            rows[heads[i]].append(content[i].text)

        if vali[heads[i]] == False:
            rows[heads[i]].append('NULL')
            
            
phones = pd.DataFrame(rows["Phone:"])

# export the data into excel file 
export = zip_longest(*rows.values())
with open ("k.csv", 'w', newline='') as file:
    w = csv.writer(file)
    w.writerow(['Company','Address', 'Phone', 'Site', 'Year', 'Facebook', 'Twitter'])
    w.writerows(export)
