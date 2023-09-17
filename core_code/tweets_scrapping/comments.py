
from googleapiclient.discovery import build
import json
import sys
import subprocess
import os
# creating youtube resource object
#youtube = build('youtube','v3',
#                developerKey="AIzaSyBHKcvgjWosmuA6onzbl0rOAAUf72S9AlM")
  
# retrieve youtube video results
#video_response=youtube.commentThreads().list(
#  part='snippet,replies',
#  videoId="JAM2yb2H3mk",
#  maxResults=100
#).execute()

def get_comments(key,version,id_video):
    youtube = build('youtube',version,developerKey = key)

    video_response=youtube.commentThreads().list(
        part='snippet,replies',
        videoId=id_video,
        maxResults = 100,
        order='time' #can change by relevance
    )
    return video_response['snippet']

def process_comments(video_response,path):
    for comment in video_response:
        filename = comment.get('id') + '.json'
        #my_path = "paolagh@132.247.186.67:public_html/static/backup/"
        with open(path+filename, 'w') as outfile:
            json.dump(comment, outfile)

def escritura_archivos():
    return
