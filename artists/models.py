from django.db import models


class Artist(models.Model):
    artist_id = models.AutoField(primary_key=True)

    stage_name = models.CharField(max_length=50, blank=False, null=False, unique=True)

    social_media_link = models.URLField(max_length=200, null=False, blank=True)

    def __str__(self):
        return self.stage_name

    class Meta:
        db_table = "Artists"
        ordering = ["stage_name"]