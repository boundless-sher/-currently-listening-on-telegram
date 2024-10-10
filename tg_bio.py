from telethon.sync import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest

import os
from dotenv import load_dotenv

import requests
import pprint
import time


load_dotenv()

FM_API_KEY = os.getenv('FM_API_KEY') 

TG_API_ID = os.getenv('TG_API_ID') 
TG_API_HASH = os.getenv('TG_API_HASH') 
tg_client = TelegramClient('anon', TG_API_ID, TG_API_HASH)
print(tg_client)





headers = {
    'user-agent': 'nowPlaying'
}
payload = {
    'api_key': FM_API_KEY,
    'method': 'user.getrecenttracks',
    'user': 'boundless-sher',
    'limit': 10,
    'format': 'json'
}


async def get_latest_songs():
    r = requests.get('https://ws.audioscrobbler.com/2.0', headers=headers, params=payload)
    status_code = r.status_code
    print('status code', status_code)
    
    if(status_code == 200):
        data = r.json()
        song_info = {}
        last_track = data['recenttracks']['track'][0]
        song_name = last_track['name']
        artist = last_track['artist']['#text']

        song_info['song_name'] = song_name
        song_info['artist'] = artist
        print('song info', song_info)
        return song_info

    else:
        print('something went wrong with last.fm api, trying again...')
        get_latest_songs()


async def update_tg_bio():
    song_info = await get_latest_songs()
    await tg_client(UpdateProfileRequest(about=f"oxirgi qo'shiq: {song_info['song_name']} - {song_info['artist']}"))
    me = await tg_client.get_me()
    print(me.stringify())


while(1):
    print('main')
    with tg_client:
        print('updating')
        tg_client.loop.run_until_complete(update_tg_bio())

    time.sleep(60 * 3)
