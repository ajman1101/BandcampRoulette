import urllib2
from BeautifulSoup import BeautifulSoup


def scrape(query):

    # Check for multiple word input
    if not isinstance(query, basestring):
        try:
            query = "+".join(query)
        except Exception as e:
            print(e)
            return None

    page = urllib2.urlopen("http://www.bandcamp.com/search?q={0}".format(
        query)).read()

    # Search bandcamp for first artist that appears from the search
    soup = BeautifulSoup(page)
    song = soup.findAll('a', href=True)[16]['href']

    # Search the first artist's page for the first song
    song_page = urllib2.urlopen(song).read()
    song_soup = BeautifulSoup(song_page)

    # Print out the url to that song
    song_player = song_soup.findAll('meta', property="og:video")[0]['content']
    return song_player
