import argparse
import json
import pprint
import sys
import urllib
import urllib2
import sys

import oauth2

API_HOST = 'api.yelp.com'
DEFAULT_TERM = ''
DEFAULT_LOCATION = 'San Jose, CA'
SEARCH_LIMIT = 3
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'

# OAuth credential placeholders that must be filled in by users.
CONSUMER_KEY = 'h0sDTTzdoafoWJu1EqBkdQ'
CONSUMER_SECRET = 'xBoIjn2UW4QzD2PhZ3ZDPWipD4w'
TOKEN = 'tgwfrjZv28T82azd2WHDNSENsIOYwAKa'
TOKEN_SECRET = 'zcfQlefNl46kpUMXclfgWmruwFA'

from bs4 import BeautifulSoup

def parse( url , lobbying):
    r = urllib.urlopen(url).read()
    soup = BeautifulSoup(r,"html.parser")
    letters = soup.find_all("article", class_="platinum")
    letters += soup.find_all("article", class_="gold")
    letters += soup.find_all("article", class_="silver")
    letters += soup.find_all("article", class_="bronze")
    letters += soup.find_all("article", class_="basic")
    for element in letters:
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




def request(host, path, url_params=None):
    """Prepares OAuth authentication and sends the request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        urllib2.HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = 'https://{0}{1}?'.format(host, urllib.quote(path.encode('utf8')))

    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request(
        method="GET", url=url, parameters=url_params)

    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': TOKEN,
            'oauth_consumer_key': CONSUMER_KEY
        }
    )
    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    oauth_request.sign_request(
        oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()

    #print u'Querying {0} ...'.format(url)
    #sys.stdout.flush()
    try:
        conn = urllib2.urlopen(signed_url, timeout = 5)
        response = json.loads(conn.read())
        conn.close()
        return response
    except:
        return None

def search(term, location):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT,
        'category_filter':'apartments'
    }
    return request(API_HOST, SEARCH_PATH, url_params=url_params)


def get_business(business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path)


def query_api(term, location, img, url, results):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """


    response = search(term, location)
    if (response == None):
        return
    businesses = response.get('businesses')

    if not businesses:
        #print u'No businesses for {0} in {1} found.'.format(term, location)
        return

    business_id = businesses[0]['id']
    print business_id
    #print u'{0} businesses found, querying business info ' \
    #    'for the top result "{1}" ...'.format(
    #        len(businesses), business_id)
    response = get_business(business_id)
    if (response == None or response['categories'][0][0]!='Apartments'):
        return
    response['realImg'] = img
    response['realUrl'] = url
    
    #print u'Result for business "{0}" found:'.format(business_id)
    #pprint.pprint(response, indent=2)
    results[business_id]=response

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('BedNum',help="The number of beds you looking for")
    parser.add_argument('MaxPrice',help="The maximum price you looking for")
    parser.add_argument('Address', help="The address")
    args = parser.parse_args()
    addressString = args.Address.replace(',',' ')
    addressString = addressString.replace(' ','-')
    #print addressString

    #parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,
    #                    type=str, help='Search term (default: %(default)s)')
    #parser.add_argument('-l', '--location', dest='location',
    #                    default=DEFAULT_LOCATION, type=str,
    #                    help='Search location (default: %(default)s)')

    inputValue ={}
    toPrint ='http://www.apartments.com/'+addressString+'/'+args.BedNum+'-beds-under-'+args.MaxPrice+'/'
    #print toPrint
    parse('http://www.apartments.com/'+addressString+'/'+args.BedNum+'-beds-under-'+args.MaxPrice+'/',inputValue)
    parse('http://www.apartments.com/'+addressString+'/'+args.BedNum+'-beds-under-'+args.MaxPrice+'/2/',inputValue)
    parse('http://www.apartments.com/'+addressString+'/'+args.BedNum+'-beds-under-'+args.MaxPrice+'/3/',inputValue)
    results = {}
    try:
        for appartments in inputValue:
            query_api(appartments, inputValue[appartments]['streetAddress']+','+inputValue[appartments]['city']+','+inputValue[appartments]['zip'], inputValue[appartments]['img'],inputValue[appartments]['url'],results)
        print json.dumps(results, ensure_ascii=False)
        #pprint.pprint(results, indent=2)
        #sorted_results = sorted(results.items(), key = lambda tup: (tup[1]["rating"]),reverse=True)
        #pprint.pprint(sorted_results, indent=2)
        #for result in sorted_results:
            #if len(result[1]['location']['address']) !=0:
                #print result#[0]+':\n\t'+"Rating: %.1f" % result[1]['rating'] + "\n\tAddress:" +result[1]['location']['address'][0] + ','+ result[1]['location']['city']+','+ result[1]['location']['state_code']
    except urllib2.HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0}. Abort program.'.format(error.code))


if __name__ == '__main__':
    main()
