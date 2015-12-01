from bs4 import BeautifulSoup
import urllib
r = urllib.urlopen('http://www.apartments.com/san-jose-ca/3-beds-under-3500/').read()
soup = BeautifulSoup(r,"html.parser")

letters = soup.find_all("article", class_="platinum")

print letters[0].find("section",class_="placardHeader")
lobbying = {}
for element in letters:
	element.find("section",class_="placards")