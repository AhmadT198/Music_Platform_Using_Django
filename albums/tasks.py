from celery import shared_task
from django.core.mail import send_mail
from musicplatform.settings import EMAIL_HOST_USER

@shared_task
def send_album_creation_email(email, album):
    send_mail(
        "Album Created Succefully !", ## Subject
        "Your Album '" + str(album['album_name']) + "' has been Created successfully!", ## Body
        EMAIL_HOST_USER, ## Host email
        [email], ## Recipient email
        fail_silently=False
    )
    print("email sent #2")

