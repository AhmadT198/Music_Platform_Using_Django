from django.db.models.signals import pre_save, pre_delete,post_save
from django.dispatch import receiver
from .models import *
from django.core.exceptions import ValidationError
from .serializers import AlbumSerializer
from .tasks import *

## Set a reciever to recieve a signal before deletion everytime the Song Model attempts to delete a song.
@receiver(pre_delete, sender=Song)
def delete_song(sender, instance, **kwargs):
    if(instance.album.songs.count() == 1): ##if this is the only Song in the Album(the Album will be empty after deletion), raise an exception.
        raise ValidationError("The Album Cannot Be Empty.")

@receiver(post_save, sender=Album)
def send_email(sender,instance, **kwargs): ## Send Email at Album Creation
    email = instance.artist.user.email
    serializer = AlbumSerializer(instance)

    send_album_creation_email.delay(email, serializer.data) ## Asynchronous Task
    print("email sent")


