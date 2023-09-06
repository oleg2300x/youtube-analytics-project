
import os

from googleapiclient.discovery import build


class Video:
    def __init__(self, video_id):
        try:
            api_key = os.getenv('API_KEY')
            youtube = build('youtube', 'v3', developerKey=api_key)
            video_info = youtube.videos().list(part='snippet, statistics', id=video_id).execute()  # Информация о видео
            self.video_result = video_info.get('items')[0]  # Меньше информации о видео
            self.video_id = video_id  # id видео
            self.title = self.video_result['snippet']['title']  # Название видео
            self.url = f'https://www.youtube.com/watch?v={video_id}'  # Сылка на видео
            self.view_count = self.video_result['statistics']['viewCount']  # Кол-во просмотров
            self.like_count = self.video_result['statistics']['likeCount']  # Кол-во лайков
        except IndexError:
            self.video_id = video_id
            self.title = None
            self.url = None
            self.like_count = None
            self.view_count = None
            self.video_result = None
            print(f'Видео с id:{self.video_id} не обнаруженно попробуйте другой id')

    def __str__(self):
        return self.title


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        api_key = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        video_info = youtube.videos().list(part='snippet,statistics', id=video_id).execute()
        result_video = video_info.get('items')[0]

        super().__init__(video_id)
        self.playlist_id = playlist_id

# video1 = Video('AWX4JnAnjBE')  # 'AWX4JnAnjBE' - это id видео из ютуб
# video2 = PLVideo('4fObz_qw9u4', 'PLv_zOGKKxVph_8g2Mqc3LMhj0M_BfasbC')
#
# print(video2)