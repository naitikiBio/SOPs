# This scrapes data from websites and stores in HTML
# Storing in HTML helps as Python hits a website multiple times, essentially creating DoS attack, and also overloads the server
# We are good people, we don't do that, and also, if the extraction is not correct, we always have the raw data to re-extract

# --- Installation ---
# Run this command in your terminal, I am assuming you already know about Python and virtual environments
# pip install requests beautifulsoup4

import requests
from bs4 import BeautifulSoup

# --- Configuration ---
url = 'your complete url here'

r = requests.get(url) # Returns the entire DOM tree
print(r.content[:100])

soup = BeautifulSoup(r.content, 'html-parser')

def save_html(html, path):
  with open(path, 'wb') as f:
    f.write(html)

save_html(r.content, 'google_com')

def open_html(path):
  with open(path, 'rb') as f:
    return f.read()

html = open_html('google_com')
