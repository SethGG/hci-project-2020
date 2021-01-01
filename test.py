from bs4 import BeautifulSoup

f = open("info.html", 'r')
html = f.read()

soup = BeautifulSoup(html, 'html.parser')
