import time
import subprocess

from django.core.management import call_command
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def backup_database():
    call_command('dbbackup', '-z')
    return 0
