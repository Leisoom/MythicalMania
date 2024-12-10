from django.db import models

# Create your models here.
class Organization(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

class Channel(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length = 30)
    youtube_link = models.CharField(max_length=30)

class Series(models.Model):
    series_id = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)

class Season(models.Model):
    season_id = models.CharField(max_length=30)
    season_number = models.IntegerField(max_length=30)
    playlist_id = models.CharField(max_length=30)
    playlist_url = models.URLField(max_length=30)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)

class Video(models.model):
    video_id = models.IntegerField(max_length=30, primary_key=True)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    youtube_videoId = models.CharField(max_length=30)
    video_url = models.URLField(max_length=30)
    publish_date = models.CharField(max_length=30)
    like_count = models.CharField(max_length=30)
    duration = models.CharField(max_length=30)

class Episode(models.Model):
    episode_id = models.IntegerField(max_length=30, primary_key=True)
    video = models.OneToOneField(Video,on_delete=models.CASCADE,)
    series_number = models.IntegerField(max_length=30)
    episode_number = models.IntegerField(max_length=30)
    season =  models.OneToOneField(Season,on_delete=models.CASCADE,)

class Link(models.Model):
    link_id = models.CharField(max_length=30)
    type = models.Choices()
    name = models.CharField(max_length=30)
