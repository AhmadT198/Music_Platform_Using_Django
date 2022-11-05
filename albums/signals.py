from django.db.models.signals import pre_save, pre_delete,post_save
from django.dispatch import receiver
from .models import *
from django.core.exceptions import ValidationError

## Set a reciever to recieve a signal before deletion everytime the Song Model attempts to delete a song.
@receiver(pre_delete, sender=Song)
def delete_song(sender, instance, **kwargs):
    if(instance.album.songs.count() == 1): ##if this is the only Song in the Album(the Album will be empty after deletion), raise an exception.
        raise ValidationError("The Album Cannot Be Empty.")

