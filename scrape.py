import sys
import urllib2
from BeautifulSoup import BeautifulSoup

# Check for two word input
if len(sys.argv) == 3:
    page = urllib2.urlopen("http://www.bandcamp.com/search?q={0}+{1}".format(
        sys.argv[1], sys.argv[2])).read()

# Check for one word input
elif len(sys.argv) == 2:
    page = urllib2.urlopen("http://www.bandcamp.com/search?q={0}".format(
        sys.argv[1])).read()

# Anything other, end the script
else:
    sys.exit()

# Search bandcamp for first artist that appears from the search
soup = BeautifulSoup(page)
song = soup.findAll('a', href=True)[16]['href']

# Search the first artist's page for the first song
song_page = urllib2.urlopen(song).read()
song_soup = BeautifulSoup(song_page)

# Print out the url to that song
song_player = song_soup.findAll('meta', property="og:video")[0]['content']
print(song_player)
