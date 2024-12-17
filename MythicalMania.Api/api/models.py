from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class Organization(models.Model):
    organization_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30)
    website_url = models.URLField()

class Channel(models.Model):
    channel_id = models.BigAutoField(primary_key=True)
    youtube_handle = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length = 30)
    channel_icon = models.URLField()
    subscriber_count = models.BigIntegerField()
    video_count = models.IntegerField()
    view_count = models.BigIntegerField()
    uploads_url = models.URLField()
    trailer_url = models.URLField()
    banner_url = models.URLField()

class Series(models.Model):
    CONTENT = "CONT"
    COMPILATION = "COM"
    MUSIC = "MUS"
    SERIES_TYPE = {
        CONTENT: "Content",
        COMPILATION: "Compilation",
        MUSIC: "Music",
    }
    series_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    isActive = models.BooleanField(default=False)
    series_type = models.CharField(
        max_length=3,
        choices= SERIES_TYPE,
        default = CONTENT
    )
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)

class Season(models.Model):
    season_id = models.BigAutoField(primary_key=True)
    season_number = models.IntegerField(max_length=30)
    playlist_id = models.CharField(max_length=30)
    playlist_url = models.URLField.null(max_length=30)
    start_date = models.DateTimeField()
    end_date = models.DateField()
    isActive = models.BooleanField(default=False)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)


class Video(models.model):
    video_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    youtube_videoId = models.CharField(max_length=30)
    youtube_id = models.CharField(max_length=30)
    publish_date = models.CharField(max_length=30)
    like_count = models.CharField(max_length=30)
    duration = models.CharField(max_length=30)

class Episode(models.Model):
    episode_id = models.BigAutoField(primary_key=True)
    series_number = models.IntegerField(max_length=30)
    episode_number = models.IntegerField(max_length=30)
    video = models.ForeignKey(Video,on_delete=models.CASCADE,)
    season =  models.ForeignKey(Season,on_delete=models.CASCADE,)

class LinkType(models.Model):
    link_type_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

class Link(models.model):
    link_id = models.BigAutoField(primary_key=True)
    url = models.URLField()
    LinkType = models.ForeignKey(LinkType, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),  # Optimize generic lookups
        ]