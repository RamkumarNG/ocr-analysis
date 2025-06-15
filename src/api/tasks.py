from celery import shared_task

import time

@shared_task
def ping_test_task():
    print("rocket started......")
    time.sleep(10)
    print("rocket stopped......")

