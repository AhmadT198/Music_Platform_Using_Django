from django.db import models

from users.models import User


class Artist(models.Model):
    artist_id = models.AutoField(primary_key=True)

    stage_name = models.CharField(max_length=50, unique=True)

    social_media_link = models.URLField(max_length=200, blank=True)

    user = models.OneToOneField(User, related_name="artist_info", on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.stage_name

    class Meta:
        db_table = "Artists"
        ordering = ["stage_name"]