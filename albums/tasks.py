from django.utils import timezone
from celery import shared_task
from django.core.mail import send_mail
from musicplatform.settings import EMAIL_HOST_USER
from artists.models import Artist
from albums.models import Album


@shared_task
def send_album_creation_email(email, album):
    send_mail(
        "Album Created Succefully !",  ## Subject
        "Your Album '" + str(album['album_name']) + "' has been Created successfully!",  ## Body
        EMAIL_HOST_USER,  ## Host email
        [email],  ## Recipient email
        fail_silently=False
    )
    print("Album Creation Email Sent")


MAX_DURATION = 30 * 24 * 60 * 60 ## 30 Days

@shared_task
def send_monthly_email():
    data = Artist.objects.all() ## Get All Artists
    now = timezone.now()
    recipients = []
    for artist in data: ## Iterate Over Each Artist

        ## Get his last_uploaded_album
        last_add_album = Album.approved_only.filter(artist_id=artist.artist_id).order_by('-created')[0]

        ## Get the duration since he last uploaded
        duration = now - last_add_album.created
        duration = round(duration.total_seconds(), 2)

        if duration >= MAX_DURATION: ## Append to the recipients list if the duration exceeds the MAX_DURATION
            recipients.append(artist.user.email)

    ## Send an Email to all the artists in the Recipient List
    send_mail(
        "Are you alright?",  ## Subject
        f''' 
        Hi There,
            We noticed you haven't uploaded any albums in the past month.
            Sadly this might negatively affect your popularity on our platform.
            We wish to see you soon.!
                                                        Best Regards.
        ''',  ## Body
        EMAIL_HOST_USER,  ## Host email
        recipients,  ## Recipient email
        fail_silently=False
    )
    print("Monthly Email Sent")
