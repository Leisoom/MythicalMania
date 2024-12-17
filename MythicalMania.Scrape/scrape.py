from googleapiclient.discovery import build
import isodate
import os
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

API_KEY = env('API_KEY');

API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


youtube = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)

#generate

#generate season using a playlist Id
def generate_season(playlist_id, series_id, is_Active = False):
    # get playlist meta data
    request = youtube.playlists().list(
        part="snippet", 
        id=playlist_id
    )
    response = request.execute()

    # get video meta data
    nextPageToken = None;
    
    #inital Request
    request = youtube.playlistItems().list(
        part="snippet,contentDetails", 
        playlistId=playlist_id,
        maxResults="50"
    )
    #inital response
    response = request.execute()

    #get nextPageToken if it exists
    nextPageToken = response.get('nextPageToken')

    #get list of video ids to then batch request them
    video_ids = list(map(lambda video: video['snippet']['resourceId']['videoId'], response['items']))

    #while nextPageToken is not None, keep request additional playlist items info
    while(nextPageToken is not None):
        request = youtube.playlistItems().list_next(request, response)
        response = request.execute()
        video_ids.extend(list(map(lambda video: video['snippet']['resourceId']['videoId'], response['items'])))
        nextPageToken = response.get('nextPageToken')

    # create chunks of 50 each for video ids for batch requesting
    video_chunks = batch(video_ids, 50)

    # store video details
    video_details_list = []

    # for each chunk, request the videos details for all videos within chunks
    for chunk in video_chunks:
        request = youtube.videos().list(
        part="id,snippet,status,statistics,contentDetails", 
        id=",".join(chunk)
        )
        response = request.execute()
        video_details_list.extend(response['items'])

    # for each video, create Episode model.
    for video in video_details_list:
        print(video['snippet']['localized']['title'])
        print(video['statistics']['viewCount'])
        print(video['statistics']['likeCount'])
        print(video['snippet']['localized']['description'])
        print(video['id'])

        print(video['snippet']['publishedAt'])

        print(isodate.parse_duration(video['contentDetails']['duration']))

        youtube.close()

def batch(resource_list, chunk_size):

  for i in range(0, len(resource_list), chunk_size):
    yield resource_list[i:i + chunk_size]

def get_channel_details(channel_id):
    request = youtube.channels().list(
        part="brandingSettings,snippet,contentDetails,statistics", 
        id=channel_id
    )
    response = request.execute()

    #General Info via Snippet
    #handle
    print(response['items'][0]['snippet']['customUrl'])
    #description
    print(response['items'][0]['snippet']['localized']['description'])
    #formatted title
    print(response['items'][0]['snippet']['localized']['title'])
    #channel created date
    print(response['items'][0]['snippet']['publishedAt'])
    #update to dynamically grab highest res thumbnail
    #channel icon
    print(response['items'][0]['snippet']['thumbnails']['high']['url'])
    
    #Stats for nerds
    #subcount
    print(response['items'][0]['statistics']['subscriberCount'])
    #view count
    print(response['items'][0]['statistics']['videoCount'])
    #rounded subcount
    print(response['items'][0]['statistics']['viewCount'])

    #contentDetails (get latest video playlist for displaying latests videos)
    #latest uploads playlist
    print(response['items'][0]['contentDetails']['relatedPlaylists']['uploads'])

    # branding media
    #trailer for channel
    print(response['items'][0]['brandingSettings']['channel']['unsubscribedTrailer'])

    #external banner (use possibly for background)
    print(response['items'][0]['brandingSettings']['image']['bannerExternalUrl'])


playlist_id = 'PLJ49NV73ttrv2fkUJ6JIoCBeu8fKI4-Dd'  
channel_id = "UC4PooiX37Pld1T8J5SYT-SQ"
#generate_season(playlist_id)
get_channel_details(channel_id);


# Add YouTube Channel