import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import asyncio

# Set your Spotify API credentials

class Recommendations():
    def __init__(self, mood):
        self.mood = mood
        self.sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='65fb68b588d548a69f232925a80bd8f1', client_secret='2281822a49e74f3f9f5137093378be17'))


        self.bases = {
            'sad': ['4uJ7lzoBiFucwTbFB4fjRZ', '6p6l4qYKD5DreLtjqHiz73', '6twYjepcAcaHVFF8AORTmE', '2JWs7c2fZ1PiNWC4xQL5v2', '7Gly3poMF6OoDPzbPsaT5z'],
            'calm': ['5nYCx7NAHQvW7ZZZeEJTTK', '6jKnJ4BZDcEJKrJhU9kumo', '7ABh21jhAp8CP9YoT8eBtz', '1xT2ud4ZFadiy0PubpRp9f', '1ePtPIG7DjX80wr30mRhNc'],
            'happy': ['0nqtu25y2SQjirn9Evbm9y', '0IrTfDgY0dF8Nzbk8M4Hdn', '5GM67uv3f4qo0XadoMnBNa', '1wcQC3Ef0xBvwGh0YXplb3', '0LkMMMYN9kmuP9ntTN9q3g']
        }

            
    async def get_playlist_by_mood(self):
        if self.mood.capitalize() == 'Sad':
            results = self.sp.recommendations(seed_tracks=self.bases.get('sad'), limit=15, target_valence=0.2)
        elif self.mood.capitalize() == 'Calm':
            results = self.sp.recommendations(seed_tracks=self.bases.get('calm'), limit=15, min_valence=0.4, max_valence=0.6)
        elif self.mood.capitalize() == 'Happy':
            results = self.sp.recommendations(seed_tracks=self.bases.get('calm'), limit=15, min_valence=0.7, max_valence=1)
        else:
            return 'Please, write one of the commands: Sad, calm, happy'
        return results


    async def get_lofi(self):
            lofi_json = []
            playlist = await self.get_playlist_by_mood()
            for track in playlist.get('tracks'):
                                lofi_json.append({
                                        'title': track['name'],
                                        'href': f'https://open.spotify.com/track/{track["id"]}'
                                }) 
            return lofi_json


# async def main():
#     test = Recommendations('sad')
#     lofi_json = await test.get_lofi()

# if __name__ == "__main__":
#     asyncio.run(main())