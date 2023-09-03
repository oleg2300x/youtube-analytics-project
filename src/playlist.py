from googleapiclient.discovery import build
import os
import isodate
import json
from datetime import datetime, timedelta

api_key = os.environ.get('API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:
    def __init__(self, playlist_id: str):
        self.playlist_id = playlist_id
        self.playlist = youtube.playlists().list(id=playlist_id, part='snippet').execute()
        self.playlist_videos = youtube.playlistItems().list(playlistId=playlist_id,
                                                            part='contentDetails,snippet',
                                                            maxResults=50,
                                                            ).execute()
        self.title = self.playlist["items"][0]["snippet"]["title"]
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(self.video_ids)).execute()

    @property
    def total_duration(self):
        total_duration = timedelta(0)

        for video in self.video_response['items']:
            duration_ISO = video['contentDetails']['duration']
            duration = str(isodate.parse_duration(duration_ISO))
            date_time_duration = datetime.strptime(duration, '%H:%M:%S')
            timedelta_duration = timedelta(hours=date_time_duration.hour,
                                           minutes=date_time_duration.minute,
                                           seconds=date_time_duration.second)
            total_duration += timedelta_duration
        return total_duration

    def show_best_video(self):
        pass

    def printj(self):
        """Выводит словарь в json-подобном удобном формате с отступами"""
        print(json.dumps(self.playlist_videos, indent=2, ensure_ascii=False))

    def show_best_video(self):
        likes_count = 0
        for video in self.video_response['items']:
            if likes_count < int(video['statistics']['likeCount']):
                likes_count = int(video['statistics']['likeCount'])
                best_video_id = video['id']

        return f"https://youtu.be/{best_video_id}"
