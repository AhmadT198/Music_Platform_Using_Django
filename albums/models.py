from django.db import models
from django.utils import timezone
from model_utils.models import TimeStampedModel
from artists.models import Artist


class Album(TimeStampedModel):
    album_id = models.AutoField(primary_key=True)

    album_name = models.CharField(max_length=500, default="New Album")

    artist = models.ForeignKey(Artist,null=False, blank=False, related_name="albums",
                               on_delete=models.CASCADE)

    album_release_date = models.DateTimeField(null=False, blank=False, default=timezone.now)

    cost = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    approved = models.BooleanField(default=False, null=False)
    def __str__(self):
        return self.album_name

    class Meta:
        db_table = "Albums"

