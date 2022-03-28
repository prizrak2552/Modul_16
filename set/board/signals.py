from distutils.command.config import config

from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from board.models import Comment


@receiver(post_save, sender=Comment)
def send_mail(sender, instance, created, **kwargs):
    if created:
        user = instance.post.author

        html = render_to_string(
            'board/messages/new_comment.html',
            {
                'user': user,
                'comment': instance,
            },
        )

        msg = EmailMultiAlternatives(
            subject=f'New response',
            from_email=config('EMAIL_HOST_USER'),
            to=[user.email]
        )

        msg.attach_alternative(html, 'text/html')
        msg.send()
    else:
        user = instance.author

        html = render_to_string(
            'board/messages/update_comment.html',
            {
                'user': user,
                'comment': instance,
            },
        )

        msg = EmailMultiAlternatives(
            subject=f'Your response received',
            from_email=config('EMAIL_HOST_USER'),
            to=[user.email]
        )

        msg.attach_alternative(html, 'text/html')
        msg.send()
