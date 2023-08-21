import spotipy
import asyncio

bases = {
    'sad': ['4uJ7lzoBiFucwTbFB4fjRZ', '6p6l4qYKD5DreLtjqHiz73', '6twYjepcAcaHVFF8AORTmE', '2JWs7c2fZ1PiNWC4xQL5v2', '7Gly3poMF6OoDPzbPsaT5z'],
    'calm': ['5nYCx7NAHQvW7ZZZeEJTTK', '6jKnJ4BZDcEJKrJhU9kumo', '7ABh21jhAp8CP9YoT8eBtz', '1xT2ud4ZFadiy0PubpRp9f', '1ePtPIG7DjX80wr30mRhNc'],
    'happy': ['0nqtu25y2SQjirn9Evbm9y', '0IrTfDgY0dF8Nzbk8M4Hdn', '5GM67uv3f4qo0XadoMnBNa', '1wcQC3Ef0xBvwGh0YXplb3', '0LkMMMYN9kmuP9ntTN9q3g']
 }          


async def get_playlist_by_mood(mood: str, playlist_name: str, token: str):
    sp = spotipy.Spotify(auth=token)
                                                           
    if mood.capitalize() == 'Sad':
        results = sp.recommendations(seed_tracks=bases.get('sad'), limit=15, target_valence=0.2)
    elif mood.capitalize() == 'Calm':
        results = sp.recommendations(seed_tracks=bases.get('calm'), limit=15, min_valence=0.4, max_valence=0.6)
    elif mood.capitalize() == 'Happy':
        results = sp.recommendations(seed_tracks=bases.get('happy'), limit=15, min_valence=0.7, max_valence=1)
    else:
        return 'Please, write one of the commands: Sad, Calm, Happy'
    
    track_ids = [f"spotify:track:{track['id']}" for track in results['tracks']]

    user_info = sp.current_user()

    user_id = user_info['id']

    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
    playlist_id = playlist.get('id')

    sp.playlist_add_items(playlist_id, track_ids)


# async def main():
#     playlist = await get_playlist_by_mood('sad')
#     return playlist

# if __name__ == "__main__":
#     asyncio.run(main())