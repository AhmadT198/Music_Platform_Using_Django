from django.db import models


class Artist(models.Model):
    artist_id = models.IntegerField(primary_key=True)
    stage_name = models.CharField(max_length=50, required=True, unique=True)
    social_media_link = models.URLField(max_length=200, null=False, blank=True)

    class Meta:
        db_table = "Artists"
        ordering = ["stage_name"]