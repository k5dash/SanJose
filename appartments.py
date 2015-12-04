from bs4 import BeautifulSoup
import urllib

def parse( url ):
	r = urllib.urlopen("http://www.apartments.com/san-jose-ca/3-beds-under-3500/2/").read()
	soup = BeautifulSoup(r,"html.parser")
	letters = soup.find_all("article")
	lobbying = {}
	element = letters[0]

	name = element.find("section",class_="placardHeader").a.get_text()
	url = element.get('data-url')
	img = element.find("div",class_="carouselInner").div.meta.get('content')
	city = element.find(itemprop="addressLocality").get_text()
	streetAddress = element.find(itemprop="streetAddress").get_text()
	zip = element.find(itemprop="postalCode").get_text()

	lobbying[name]={}
	lobbying[name]['url'] = url 
	lobbying[name]['img'] = img
	lobbying[name]['streetAddress'] = streetAddress
	lobbying[name]['city'] = city
	lobbying[name]['zip'] = zip
	return lobbying

	
def main():
	parse('http://www.apartments.com/san-jose-ca/3-beds-under-3500/')
	parse('http://www.apartments.com/san-jose-ca/3-beds-under-3500/2/')

if __name__ == "__main__":
    main()