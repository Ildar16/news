from django.core.mail import EmailMultiAlternatives
from celery import shared_task
from celery.schedules import crontab


@shared_task
def email_task(subscriber_username, subscriber_email, html_content):
    msg = EmailMultiAlternatives(
                    subject=f'Здравствуй, {subscriber_username}. Новая статья в вашем разделе!',
                    from_email='ildark116@yandex.ru',
                    to=[subscriber_email]
                )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def weekly_email_task(subscriber_username, subscriber_email, html_content):
    msg = EmailMultiAlternatives(
        subject=f'Здравствуй, {subscriber_username}, новые статьи за прошлую неделю в вашем разделе!',
        from_email='ildark116@yandex.ru',
        to=[subscriber_email]
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
