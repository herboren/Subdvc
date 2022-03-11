from urllib import response
from bs4 import BeautifulSoup
import requests, re, os
from colorama import *


G = Fore.LIGHTGREEN_EX  # green
Y = Fore.LIGHTYELLOW_EX  # yellow
B = Fore.LIGHTBLUE_EX  # blue
R = Fore.LIGHTRED_EX  # red
W = Fore.LIGHTWHITE_EX  # white
C = Fore.LIGHTCYAN_EX # Cyan


# Url used to obtain valid domain certificates
crt = 'https://crt.sh/?q='
parameter = ''

# Custom Header (https://httpbin.org/get)
header = {
    "Accept": "*/*",     
    "Accept-Language": "en-US,en;q=0.9", 
    "DNT": "1",        
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36", 
    "Referer":"https://www.duckduckgo.com"
}

# Requires status 200
def GetStatus(status):
    response = requests.get('https://'+status)
    return True if response.status_code == 200 else False

# Get user input
dirty = input("Input domain name (ex: https://mit.edu): ")

# Need to get second+top level only
if "/" in dirty:
        clean = re.sub('((https?|ftp|file):\/{2,})|(www\.)','', dirty)        
        parameter = clean.split('/')[0]            
        print(f"{G}\nWorking url: {W}{crt}{parameter}")

try:
    subdomains = [] # Get table rows, listo f list

    # Get page data
    if GetStatus(parameter):
        response = requests.get(crt+parameter, headers=header)
        soup = BeautifulSoup(response.text, 'html.parser')
        trows = soup.find_all('tr')
        
        # Get 5 element of table data in table row
        for row in trows:
            cols = row.find_all('td')[5:6]
            cols=[x.text for x in cols]
            subdomains.append(cols)   

        rgx_domain = '' # Build a long string
        dom_nodupe = [] # Holds non-dupe entries

        # Regex remove uneccesary SYMBOLS
        for sd in subdomains:
            # . and - allowed in subdomain
            rgx_domain += re.sub('([wW]{3,3}\.)|[\*]\.|([^\w+\-\.])','', str(sd))            
        
        # Split subdomains at second+top level
        rgx_domain = rgx_domain.split(parameter)        

        # Check for empty entries
        for domain in rgx_domain:
            if len(str(domain)) != 0:
                if domain not in dom_nodupe:                    
                    dom_nodupe.append(domain)

        # Write entries to file
        if not os.path.isfile(parameter + ".txt"):
            with open(parameter + ".txt", "a", encoding='utf-8') as f:
                for d in dom_nodupe:           
                    f.write(str(d.strip('.')) + "\n")
                         
        print(f"{C}Sub-domains written to file: {parameter}.txt{W}")

except Exception as ex:
    print(ex)

