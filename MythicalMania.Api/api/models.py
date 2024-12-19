from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Organization(models.Model):
    organization_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150)
    website_url = models.URLField()

class Channel(models.Model):
    channel_id = models.BigAutoField(primary_key=True)
    youtube_handle = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30)
    description = models.TextField()
    channel_icon = models.URLField()
    subscriber_count = models.BigIntegerField()
    video_count = models.BigIntegerField()
    view_count = models.BigIntegerField()
    uploads_youtube_playlist_id = models.CharField(max_length=30)
    featured_video_id = models.CharField(max_length=30)
    banner_url = models.URLField()

class Video(models.Model):
    video_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    youtube_id = models.CharField(max_length=30)
    publish_date = models.DateTimeField()
    like_count = models.BigIntegerField()
    duration = models.BigIntegerField()

class Media(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class Series(Media):
    series_id = models.BigAutoField(primary_key=True)
    isActive = models.BooleanField(default=False)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
class Show(models.Model):

    show_id = models.BigAutoField(primary_key=True)
    isActive = models.BooleanField(default=False)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    youtube_playlist_id = models.CharField(max_length=30, blank=True)

    class Meta:
        abstract = True

class SeasonalShow(Show):
    title = models.CharField(max_length=255)
    description = models.TextField()
    season_number = models.IntegerField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

class Podcast(Show):
    spotify_show_id = models.CharField(max_length=30, blank=True)

class Episode(models.Model):
    episode_id = models.BigAutoField(primary_key=True)
    episode_number = models.PositiveIntegerField()
    video = models.ForeignKey(Video,null=True, blank=True,on_delete=models.CASCADE,)

    class Meta:
        abstract = True

class SeasonalEpisode(Episode):
    show = models.ForeignKey(SeasonalShow, null=True, blank=True, on_delete=models.CASCADE)
    overall_series_episode_number = models.PositiveIntegerField()

class PodcastEpisode(Episode):
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE,)
    spotify_id = models.CharField(max_length=30)
    #addtional spotify data

class LinkType(models.Model):
    link_type_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

class Link(models.Model):
    link_id = models.BigAutoField(primary_key=True)
    url = models.URLField()
    link_type = models.ForeignKey(LinkType, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),  # Optimize generic lookups
        ]