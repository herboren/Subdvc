from getpass import getuser
from signal import default_int_handler
from urllib import response
from bs4 import BeautifulSoup
import requests, re

usrdomain = ''
subdomains = []

# Url
crt = 'https://crt.sh/?q='
parameter = ''

# Header
header = {
    "Accept": "*/*",     
    "Accept-Language": "en-US,en;q=0.9", 
    "DNT": "1",        
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36", 
    "Referer":"https://www.duckduckgo.com"
}

# Used for crt.sh concatenation
def GetUserInput():
    dirty = input("Input domain name (ex: mit.edu): ")
    print(dirty)
    if "/" in dirty:
        clean = re.sub('((https?|ftp|file):\/{2,})|(www\.)','', dirty)        
        clean = clean.split('/')
        return clean[0]

# Requires http protocol
def GetStatus(status):
    response = requests.get('https://'+status)
    return True if response.status_code == 200 else False

try:
    if GetStatus(GetUserInput()):
        response = requests.get(crt, headers=header)
        soup = BeautifulSoup(response.content, 'html.parser')
        trows = soup.find_all('td')[5:6]

        for r in trows:
            print(r)

except Exception as ex:
    print(ex)

