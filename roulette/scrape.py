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
    try:
        song = soup.find('li', 'searchresult').a['href']
    except AttributeError:
        return None

    # Search the first artist's page for the first song
    try:
        song_page = urllib2.urlopen(song).read()
        song_soup = BeautifulSoup(song_page)
    except Exception as e:
        print(e)
        return None

    # Print out the url to that song
    song_player = song_soup.find('meta', property="og:video")
    if song_player:
        song_player = song_player['content']
        song_title = song_soup.find('meta', property="og:title")['content']

    # If the first item is an artist, access the first album
    else:
        album = song + song_soup.find('div', 'ipCellSet').find('a')['href']
        album_page = urllib2.urlopen(album).read()
        album_soup = BeautifulSoup(album_page)
        song_player = album_soup.find('meta', property="og:video")['content']
        song_title = album_soup.find('meta', property="og:title")['content']

    return (song_player, song_title)
