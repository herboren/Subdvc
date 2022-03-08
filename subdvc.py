from urllib import request
from bs4 import BeautifulSoup
import requests, bs4, urllib
import re, os

# Make corrections
def GetSecondTopLevel(domain):
    return re.sub('^[^\w+]|[^\w+\-\.]|[^\w+]$','',domain)

domain = GetSecondTopLevel(input("Input second and top level domain (site.edu): "))
subdomains = []

# Search current/expired cert for domain
crt = 'https://crt.sh/?q=' + domain

# Custom Header
header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
    "Accept-Encoding": "gzip, deflate, br", 
    "Accept-Language": "en-US,en;q=0.9", 
    "Host": "httpbin.org", 
    "Sec-Ch-Ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"99\", \"Google Chrome\";v=\"99\"", 
    "Sec-Ch-Ua-Mobile": "?0", 
    "Sec-Ch-Ua-Platform": "\"Windows\"", 
    "Sec-Fetch-Dest": "document", 
    "Sec-Fetch-Mode": "navigate", 
    "Sec-Fetch-Site": "none", 
    "Sec-Fetch-User": "?1", 
    "Upgrade-Insecure-Requests": "1", 
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36", 
    "X-Amzn-Trace-Id": "Root=1-6226be72-115409e058feb2d26668c850"
  }

try:
    print("Getting subdomains, from ["+crt+"]")
    # Get response, return status, if true, proceed
    response = requests.get(crt, headers=header)
    if response.status_code == 200:
        # Getting page data       
        soup = BeautifulSoup(response.content, 'html.parser')
        tbody = soup.find('tbody')
        trows = tbody.find_all('tr')

        for row in trows:
            cols = row.find_all('td')
            cols = [x.text.strip() for x in cols]
            subdomains.append(cols)
        
        
        #print("Dumping subdomains to " + domain.split('.')[0] + ".txt")
        for r in subdomains:
            print(r)
            #with open(domain.split('.')[0] + ".txt", "a", encoding='utf-8') as f:
            #    f.write(re.sub('\u200f|\u200e', "", a.text) + "\n")
except:
    print("There was an error processed your request::" + response.status_code)
