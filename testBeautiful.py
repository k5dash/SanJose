from bs4 import BeautifulSoup
import urllib
r = urllib.urlopen('http://www.aflcio.org/Legislation-and-Politics/Legislative-Alerts').read()
soup = BeautifulSoup(r,"html.parser")
letters = soup.find_all("div", class_="ec_statements")
##print letters[0].prettify()

lobbying = {}
for element in letters:
    lobbying[element.a.get_text()] = {}

prefix = "www.aflcio.org"

for element in letters:
    lobbying[element.a.get_text()]["link"] = prefix + element.a["href"]

for element in letters:
    date = element.find(id="legalert_date").get_text()
    lobbying[element.a.get_text()]["date"] = date

#for item in lobbying.keys():
#   print item + ": " + "\n\t" + "link: " + lobbying[item]["link"] + "\n\t" + "date: " + lobbying[item]["date"] + "\n\n" 

import json
writeJSON ={}
json.dump(lobbying, writeJSON)

print writeJSON