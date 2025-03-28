import os
import requests
import json
#response = requests.get("http://localhost:8080/getytaudio",params={"url":"https://www.youtube.com/watch?v=AHLFNoT64HQ&pp=ygUTZW5kbGVzcyBmcmFuayBvY2Vhbg%3D%3D"})
#print(response.json())
class CaesarAIMusicSpotifyRecommendendation:
    def __init__(self):
        body = {
            "grant_type":"client_credentials",
            "client_id": "ee68fd6ea6bb4173b1280b4e10413505",
            "client_secret":"5fca46453288405c97b6cbd69916a63d"
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.directory = 'Recommendations'
    

        response = requests.post('https://accounts.spotify.com/api/token', data=body,headers=headers)
        self.access_token = response.json()["access_token"]
        self.access_token_headers = {"Authorization": f"Bearer {self.access_token}"}
    def search_user(self,query):
        response = requests.get("https://api.spotify.com/v1/search",params={"q":query,"type":"track"},headers=self.access_token_headers)
        return response.json()
    def get_audio_features(self,id):
        response = requests.get(f"https://api.spotify.com/v1/audio-features/{id}",headers=self.access_token_headers)
        return response.json()
    def clean_features(self,data):
        final_data = {'target_danceability': data["danceability"], 'target_energy': data["energy"], 'target_key': data["key"], 'target_loudness': data["loudness"], 'target_mode': data["mode"], 'target_speechiness':data["speechiness"], 'target_acousticness': data["acousticness"], 'target_instrumentalness': data["instrumentalness"], 'target_liveness': data["liveness"], 'target_valence': data["valence"], 'target_tempo':data["tempo"] }
        return final_data
    def get_recommendation(self,id,data):
        data["limit"] = 50
        data["seed_tracks"] = id
        response = requests.get(f"https://api.spotify.com/v1/recommendations",params=data,headers=self.access_token_headers)
        return response.json()
    def extract_recommendation(self,recommendations):
        track_recommendations = []
        for track in recommendations:
            #del 

            new_track = {key:val for key, val in track.items() if key != 'available_markets'}
            del new_track["album"]["available_markets"]
            track_recommendations.append({"name":new_track["name"],"artist":new_track["album"]["artists"][0]["name"]})
        return track_recommendations
    def store_recommendation(self,recommendations):
        if not os.path.isdir(self.directory):
            os.mkdir(self.directory)
        if not os.path.isfile(f"{self.directory}/recommendations.json"):                
            with open(f"{self.directory}/recommendations.json","w+") as f:
                json.dump({"recommendations":[{"tracks":recommendations}]},f)
        else:
            with open(f"{self.directory}/recommendations.json","r") as f:
                track_rec_read = json.load(f)
            track_rec_read["recommendations"].append({"tracks":recommendations})
            with open(f"{self.directory}/recommendations.json","w") as f:
                json.dump(track_rec_read,f)


                

        



caesaraimusicsp = CaesarAIMusicSpotifyRecommendendation()
song_id = caesaraimusicsp.search_user("Resentment PARTYNEXTDOOR")["tracks"]["items"][0]["id"]

features = caesaraimusicsp.get_audio_features(song_id)
final_features = caesaraimusicsp.clean_features(features)
recommendations = caesaraimusicsp.get_recommendation(song_id,final_features)["tracks"]
extracted_recommendations = caesaraimusicsp.extract_recommendation(recommendations)


caesaraimusicsp.store_recommendation(extracted_recommendations)
