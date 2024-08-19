
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import yaml

# Load credentials
with open("spotify.yaml", "r") as stream:
    spotify_details = yaml.safe_load(stream)

# Set up Spotify client
auth_manager = SpotifyClientCredentials(
    client_id=spotify_details['Client_id'],
    client_secret=spotify_details['client_secret']
)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Streamlit app
st.title("Spotify Music Recommendation System")

# Function to get track ID from track name
def get_track_id(track_name):
    result = sp.search(q=track_name, type='track', limit=1)
    tracks = result['tracks']['items']
    if tracks:
        return tracks[0]['id']
    return None

# Function to get recommendations
def recommend_tracks(seed_tracks):
    seed_track_ids = [get_track_id(track) for track in seed_tracks if get_track_id(track)]
    if not seed_track_ids:
        return []
    recommendations = sp.recommendations(seed_tracks=seed_track_ids, limit=10)
    return recommendations['tracks']

# User input
seed_tracks_input = st.text_input("Enter seed track names (comma-separated):")
if st.button('Get Recommendations'):
    seed_tracks_list = [track.strip() for track in seed_tracks_input.split(',')]
    recommendations = recommend_tracks(seed_tracks_list)
    if recommendations:
        for track in recommendations:
            st.write(f"{track['name']} by {', '.join([artist['name'] for artist in track['artists']])}")
    else:
        st.write("No recommendations found.")
