import sys, requests, subprocess
from bs4 import BeautifulSoup
from constants import (
    TOKEN
)

defaults = {
    'request': {
        'token': TOKEN,
        'base_url': 'https://api.genius.com'
    },
    'message': {
        'search_fail': 'The lyrics for this song were not found!',
        'wrong_input': 'Wrong number of arguments.\n' \
                       'Use two parameters to perform a custom search ' \
                       'or none to get the song currently playing on Spotify, iTunes, or Sonos.',
        'connection_issue': 'There was a problem connecting to the Sonos service'
    },
    'response': {
        'artist': '', 
        'title': ''
    }
}


def get_current_song_info():
    song = get_current_sonos_song_info()

    if not song:
        song = get_current_itunes_song_info()

    return song

def get_current_sonos_song_info():
    # This is a URL to a running instance of https://github.com/jishi/node-sonos-http-api
    node_sonos_url = 'http://localhost:5005/state'
    # At some point, need to add a check for playbackState!
    try:
        metadata = requests.get(node_sonos_url)
        current_track = metadata.json()['currentTrack']
    except:
        print(defaults['message']['connection_issue'])
        return

    return {'artist': current_track['artist'], 'title': current_track['title']}

def get_current_itunes_song_info():
    # Note that this will only work on macOS/OSX!
    current_track = subprocess.check_output(['osascript', 'current_itunes_song.applescript'])
    split = current_track.decode().split(" || ")
    song_artist = split[0]
    song_name = split[1]
    return {'artist': song_artist.rstrip(), 'title': song_name.rstrip()}

def request_song_info(song_title, artist_name):
    base_url = defaults['request']['base_url']
    headers = {'Authorization': 'Bearer ' + defaults['request']['token']}
    search_url = base_url + '/search'
    data = {'q': song_title + ' ' + artist_name}
    response = requests.get(search_url, data=data, headers=headers)

    return response

def scrap_song_url(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    [h.extract() for h in html('script')]
    lyrics = html.find('div', class_='lyrics').get_text()

    return lyrics

def main():
    args_length = len(sys.argv)
    if args_length == 1:
        # Get info about song currently playing on Spotify
        current_song_info = get_current_song_info()
        song_title = current_song_info['title']
        artist_name = current_song_info['artist']
    elif args_length == 3:
        # Use input as song title and artist name
        song_info = sys.argv
        song_title, artist_name = song_info[1], song_info[2]
    else:
        print(defaults['message']['wrong_input'])
        return

    print('{} by {}'.format(song_title, artist_name))

    # Search for matches in request response
    response = request_song_info(song_title, artist_name)
    json = response.json()
    remote_song_info = None

    for hit in json['response']['hits']:
        if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
            remote_song_info = hit
            break

    # Extract lyrics from URL if song was found
    if remote_song_info:
        song_url = remote_song_info['result']['url']
        lyrics = scrap_song_url(song_url)

        write_lyrics_to_file(lyrics, song_title, artist_name)

        print(lyrics)
    else:
        print(defaults['message']['search_fail'])

def write_lyrics_to_file (lyrics, song, artist):
    f = open('lyric-view.txt', 'w')
    f.write('{} by {}'.format(song, artist))
    f.write(lyrics)
    f.close()

if __name__ == '__main__':
    main()
