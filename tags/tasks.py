from __future__ import absolute_import

from celery import shared_task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from .models import Tag
from django.utils import timezone
import datetime


@periodic_task(run_every=(crontab(minute='*/300')), name="delete_tags", ignore_result=True)
def delete_tags():
    oldtags = Tag.objects.filter(
        created__lte=timezone.now() + datetime.timedelta(days=-1))
    oldtags.delete()
