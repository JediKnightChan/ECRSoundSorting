import time

from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def sleep_and_wait():
    time.sleep(600)
    print("Hello world")
