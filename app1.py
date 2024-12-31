import streamlit as st
import pickle
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials
CLIENT_ID = "5579d0adf9f24a0db020acf55959c86a"
CLIENT_SECRET = "8ccfebd23c0c4352833d7358dae0807d"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Function to get album cover URL
def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"


# Function to recommend songs
def recommendation(song_title):
    filtered_df = music[music['song'] == song_title]
    
    if filtered_df.empty:
        return f"The song '{song_title}' was not found in the DataFrame."
    
    idx = filtered_df.index[0]
    distances = sorted(list(enumerate(similarity[idx])), reverse=True, key=lambda x: x[1])
    
    recommended_music_names = []
    recommended_music_posters = []
    for m_id in distances[1:6]:  # 1 to 6 to get top 5 recommendations
        recommended_music_names.append(music.iloc[m_id[0]].song)
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[m_id[0]].song, music.iloc[m_id[0]].artist))
    
    return recommended_music_names, recommended_music_posters

st.header('Music Recommender System')

try:
    music = pickle.load(open('df.pkl', 'rb'))
    st.write("Loaded music data successfully")
except Exception as e:
    st.write(f"Error loading music data: {e}")

try:
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    st.write("Loaded similarity data successfully")
except Exception as e:
    st.write(f"Error loading similarity data: {e}")
if 'music' in locals() and 'similarity' in locals():
    music_list = music['song'].values
    selected_song = st.selectbox(
        "Type or select a song from the dropdown",
        music_list
    )
    st.write(f"Selected song: {selected_song}")
    if st.button('Show Recommendation'):
        recommendations = recommendation(selected_song)
        if isinstance(recommendations, str):
            st.write(recommendations)
        else:
            recommended_music_names, recommended_music_posters = recommendations
            cols = st.columns(5)
            for col, name, poster in zip(cols, recommended_music_names, recommended_music_posters):
                with col:
                    st.text(name)
                    st.image(poster)
else:
    st.write("Music data or similarity data is not loaded.")