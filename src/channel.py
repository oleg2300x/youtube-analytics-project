
import os
import json
from googleapiclient.discovery import build

class Channel:
    """Класс для ютуб-канала"""
    api_key = os.environ.get('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = self.channel["items"][0]["snippet"]["title"]
        self.description = self.channel["items"][0]["snippet"]["description"]
        self.url = f"https://www.youtube.com/channel/{self.channel_id}"
        self.count_subscribers = self.channel["items"][0]["statistics"]["subscriberCount"]
        self.video_count = self.channel["items"][0]["statistics"]["videoCount"]
        self.count_views = self.channel["items"][0]["statistics"]["viewCount"]

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return cls.youtube

    def to_json(self, file_name):
        with open(file_name, 'w') as y_file:
            json.dump(self.__dict__, y_file)
