import requests
from datetime import datetime as dt
from datetime import date
import datetime
import pprint
import pandas as pd
import sqlite3

USER_ID = 'neider321'
TOKEN_ID = 'BQAEztrud3ETBmBeFhzZET7qT624wbPpW9JCUHStqlWwFmrBeblBE1YeNjQPz-h7EnHrwwk_GbrBRmRkh9LDQJaHYBr-QwV8Z39HUd_SeuWlKY_fVtTJuZS8EFViX6d1JmjIIAnZ0VghrBxXT2lErfEMSQDB8AISdfeLgR0K0ZAGmOiOyOqdK9S2-ywPEyB5bjO1OHB9mZpwmWJ9yTPeqo9kYGl5KQ5kOL_QRzyA-nJpjB4uKpQBWKtzAgPVWwrmQQ'
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Bearer {token}".format(token=TOKEN_ID)
}

def get_date():
    today = dt.now()
    day = today - datetime.timedelta(days=1)
    return day


def check_data(df: pd.DataFrame):
    #check if empty
    if df.empty:
        return False
    #check nulls
    if df.isnull().values.any():
        raise Exception('Nulls are here!')
    return True
    # after i set up when i will run the program
    #check if all of dates are from yesterday, if not - drop these rows
  #  timestamps = df["timestamp"].tolist()
  #  yesterday = dt.combine(get_date(), dt.min.time())
  #  for timestamp in timestamps:
  #      if datetime.datetime.strptime(timestamp, '%Y-%m-%d') != yesterday:
  #          raise Exception("At least one of the returned songs does not have a yesterday's timestamp")




def download_songs_data(headers):

    yesterday_unix_timestamp = int(get_date().timestamp()) * 1000
    # Downloads 50 last songs you listened to yesterday.
    r = requests.get(f"https://api.spotify.com/v1/me/player/recently-played?limit=50&after={yesterday_unix_timestamp}", headers = headers)

    print(r)
    data = r.json()
    artists = []
    artist_id = []
    song_title = []
    album_name = []
    play_timestamp = []
    for num in data['items']:
        artists.append(num['track']['artists'][0]['name'])
        artist_id.append(num['track']['artists'][0]['id'])
        song_title.append(num['track']['name'])
        album_name.append(num['track']['album']['name'])
        play_timestamp.append(num['played_at'])

    dict = {
        'artist':artists,
        'artist_id':artist_id,
        'song_title':song_title,
        'album_name':album_name,
        'Date_played':play_timestamp
    }
    return dict



def get_artists_details(artistIDlist):
    #zwraca listę gatunków danych artystów.
    artist_genre = []
    for artist in artistIDlist:
        r = requests.get(f"https://api.spotify.com/v1/artists/{artist}", headers=headers)
       # print(artist)
        data = r.json()
        if len(data['genres']) > 0:
            artist_genre.append(data['genres'][0])
        else:
            artist_genre.append('No Genre')
    dict = {
        'Artist_Genre': artist_genre
    }
    return dict

    def insert_into_sql():
        #tu napisac inserta do sql'a
        #sprawdzic jak sqlalchemy bedzie to insertowac
        #ogarnac jakas free bazke sql

if __name__ == '__main__':
    songs_dict = download_songs_data(headers)
    artist_genres = get_artists_details(songs_dict['artist_id'])
    songs_dict.update(artist_genres) # update songs genres
    df = pd.DataFrame.from_dict(songs_dict)

    if check_data(df):
        print('everythink is ok')



    #print(df)
# download artist gendre, done
# put it into df done
# connect 2 df's done
# upload it to sql server
# get scheduling
# get tableau analytics