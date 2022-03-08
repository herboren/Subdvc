from urllib import request
import requests, bs4
import re, os

# Search current/expired cert for domain
crt = 'https://crt.sh/?q='

# Custom Header
header = {
    "Accept": "*/*",     
    "Accept-Language": "en-US,en;q=0.9", 
    "DNT": "1",        
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 S afari/537.36", 
    "Referer":"https://www.duckduckgo.com"
}

# Get Response
response = request.get(crt, headers=header)
soup = BeautifulSoup(response.content, 'html.parser')
tbody = soup.find('tbody')
for a in tbody.find_all('a'):
    with open("level_domains.txt", "a", encoding='utf-8') as f:
        f.write(re.sub('\u200f|\u200e', "", a.text) + "\n")