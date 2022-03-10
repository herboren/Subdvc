from posixpath import split
from urllib import response
from bs4 import BeautifulSoup
import requests, re

is_windows = sys.platform.startswith('win')

# Console Colors
if is_windows:
    # Windows deserves coloring too :D
    G = '\033[92m'  # green
    Y = '\033[93m'  # yellow
    B = '\033[94m'  # blue
    R = '\033[91m'  # red
    W = '\033[0m'   # white
    try:
        import win_unicode_console , colorama
        win_unicode_console.enable()
        colorama.init()
        #Now the unicode will work ^_^
    except:
        print("[!] Error: Coloring libraries not installed, no coloring will be used [Check the readme]")
        G = Y = B = R = W = G = Y = B = R = W = ''


else:
    G = '\033[92m'  # green
    Y = '\033[93m'  # yellow
    B = '\033[94m'  # blue
    R = '\033[91m'  # red
    W = '\033[0m'   # white

def no_color():
    global G, Y, B, R, W
    G = Y = B = R = W = ''

# Url
crt = 'https://crt.sh/?q='
parameter = ''
toplevel = ''
# Header
header = {
    "Accept": "*/*",     
    "Accept-Language": "en-US,en;q=0.9", 
    "DNT": "1",        
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36", 
    "Referer":"https://www.duckduckgo.com"
}

# Requires http protocol for status
def GetStatus(status):
    response = requests.get('https://'+status)
    return True if response.status_code == 200 else False

dirty = input("Input domain name (ex: https://mit.edu): ")
if "/" in dirty:
        clean = re.sub('((https?|ftp|file):\/{2,})|(www\.)','', dirty)        
        parameter = clean.split('/')[0]            
        print("Working url: "+crt+parameter)

try:
    subdomains = []
    domainlist = []
    
    if GetStatus(parameter):
        response = requests.get(crt+parameter, headers=header)
        soup = BeautifulSoup(response.text, 'html.parser')
        trows = soup.find_all('tr')
        
        for row in trows:
            cols = row.find_all('td')[5:6]
            cols=[x.text for x in cols]
            subdomains.append(cols)   

        rstr = ''

        for row in subdomains: 
            rstr += str(row)         
            rstr = re.sub('[^\w+\-\.]', '', rstr)
        
        subdomains = rstr.split('.' + parameter)
        for row in subdomains: 
            if len(row) > 1:
                if row not in domainlist:                
                    domainlist.append(row)
        
        with open(parameter + ".txt", "a", encoding='utf-8') as f:
            for domain in domainlist:
                f.write(str(domain) + "\n")

except Exception as ex:
    print(ex)

