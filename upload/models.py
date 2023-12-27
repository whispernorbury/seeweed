from django.db import models

# Create your models here.
class DatabaseText(models.Model):
    database_text_title = models.TextField(blank=True)
    database_text_number = models.IntegerField(blank=True)
    database_text_content = models.TextField(blank=True)

class DatabaseImage(models.Model):
    database_image_title = models.TextField(blank=True)
    database_image_number = models.IntegerField(blank=True)
    database_image_content = models.URLField(blank=True)

class DatabaseAudio(models.Model):
    database_audio_title = models.TextField(blank=True)
    database_audio_number = models.IntegerField(blank=True)
    database_audio_content = models.TextField(blank=True)
