from urllib import request
from bs4 import BeautifulSoup
import requests, bs4, urllib
import re, os

# Make corrections
def GetSecondTopLevel(domain):
    return re.sub('^[^\w+]|[^\w+\-\.]|[^\w+]$','',domain)

domain = GetSecondTopLevel(input("Input second and top level domain (site.edu)"))
subdomains = []

# Search current/expired cert for domain
crt = 'https://crt.sh/?q=' + domain

# Custom Header
header = {
    "Accept": "*/*",     
    "Accept-Language": "en-US,en;q=0.9", 
    "DNT": "1",        
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 S afari/537.36", 
    "Referer":"https://www.duckduckgo.com"
}

try:
    print("Getting subdomains, please wait")

    # Get response, return status, if true, proceed
    response = requests.get(crt, headers=header)
    if (response.status_code == 200):
        # Getting page data       
        soup = BeautifulSoup(response.content, 'html.parser')
        tbody = soup.find('tbody')
        trows = tbody.find_all('tr')

        for row in trows:
            cols = row.find_all('td')
            cols = [x.text.strip() for x in cols]
            subdomains.append(cols)
        
        
        #print("Dumping subdomains to " + domain.split('.')[0] + ".txt")
        for a in tbody.find_all('a'):
            print(a)
            #with open(domain.split('.')[0] + ".txt", "a", encoding='utf-8') as f:
            #    f.write(re.sub('\u200f|\u200e', "", a.text) + "\n")
except:
    print("There was an error processed your request::" + response.status_code)
