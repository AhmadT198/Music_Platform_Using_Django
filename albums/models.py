from django.db import models
from django.utils import timezone
from model_utils.models import TimeStampedModel
from artists.models import Artist
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class ApprovedAlbumsManager(models.Manager):
    ''' Custom Manager to Display only Approved Albums '''
    def get_queryset(self):
        return super().get_queryset().filter(approved=True)


class Album(TimeStampedModel):
    album_id = models.AutoField(primary_key=True)

    album_name = models.CharField(max_length=500, default="New Album")

    artist = models.ForeignKey(Artist,null=False, blank=False, related_name="albums",
                               on_delete=models.CASCADE)

    album_release_date = models.DateTimeField(null=False, blank=False, default=timezone.now)

    cost = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    approved = models.BooleanField(default=False, null=False)

    approved_only = ApprovedAlbumsManager() ## Defining Custom Manager

    def __str__(self):
        return self.album_name

    class Meta:
        db_table = "Albums"

class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="songs")
    name = models.CharField(max_length=250, blank=True, null=True)
    image = models.ImageField(upload_to='pics',null=False, blank=False)
    image_thumbnail = ImageSpecField(source='image', processors=[ResizeToFill(100,50)], format='JPEG', options={'quality' : 60})
    audio_file = models.FileField(upload_to='audio',null=False, blank=False)

    class Meta:
        db_table = 'songs'
