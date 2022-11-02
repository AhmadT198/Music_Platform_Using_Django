from django.db import models
from django.utils import timezone

from artists.models import Artist


class Album(models.Model):
    album_id = models.AutoField(primary_key=True)

    album_name = models.CharField(max_length=500, default="New Album")

    artist = models.ForeignKey(Artist,null=False, blank=False, related_name="albums",
                               on_delete=models.CASCADE)

    date_created = models.DateTimeField(auto_now_add=True)

    album_release_date = models.DateTimeField(null=False, blank=False, default=timezone.now)

    cost = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)

    class Meta:
        db_table = "Albums"
