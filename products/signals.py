import json

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask, CrontabSchedule

from .models import Brand


@receiver(post_save, sender=Brand)
def create_periodic_task(sender, instance, created, **kwargs):
    if created:
        schedule, _ = CrontabSchedule.objects.get_or_create(minute='0', hour='*/6')
        PeriodicTask.objects.create(
            crontab=schedule,
            name=f'scrape_brand_{instance.id}',
            task='scraper.tasks.scrape_brand_task',
            args=json.dumps([instance.id]),
        )


@receiver(post_delete, sender=Brand)
def delete_periodic_task(sender, instance, **kwargs):
    PeriodicTask.objects.filter(name=f'scrape_brand_{instance.id}').delete()
