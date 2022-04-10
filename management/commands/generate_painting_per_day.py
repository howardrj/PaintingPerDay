import logging
import requests
import json
import datetime
from datetime import datetime, timedelta, date, time
from time import sleep

from django.conf import settings
from django.core.management.base import BaseCommand

from painting_per_day.models import Painting

logger = logging.getLogger(settings.PROJECT_NAME)

class Command(BaseCommand):

    COMMAND_SLEEP_TIME_AFTER_ERROR = 10
    def add_arguments (self, parser):
        pass

    def seconds_until_tomorrow (self):

        # From https://dev.to/vladned/calculating-the-number-of-seconds-until-midnight-383d
        now = datetime.now()
        midnight = datetime.combine(now + timedelta(days=1), time())

        return (midnight - now).seconds + 1

    def handle (self, *args, **options):

        while True:

            logger.info("Checking if new painting needs to be generated")

            current_date = date.today().strftime('%Y-%m-%d')

            if len(Painting.objects.all().filter(date_selected=current_date)):

                seconds_to_wait = self.seconds_until_tomorrow()

                logger.error("Painting already exists for %s. Trying again in %d seconds",
                             current_date, seconds_to_wait)
                             
                sleep(seconds_to_wait)
                continue

            # TODO Generate painting

            seconds_to_wait = self.seconds_until_tomorrow()

            sleep(seconds_to_wait)
