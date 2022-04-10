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
    COMMAND_RANDOM_PAINTING_URL = 'https://api.artsy.net/api/artworks?sample=1&page=1'
    COMMAND_API_TOKEN_URL = 'https://api.artsy.net/api/tokens/xapp_token?client_id=%s&client_secret=%s' % \
        (settings.ARTSY_CLIENT_ID, settings.ARTSY_CLIENT_SECRET)

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

            # Get API token
            try:
                response = requests.post(self.COMMAND_API_TOKEN_URL)
            except Exception as e:
                logger.error("Failed to retrieve API token - %s", e)
                sleep(self.COMMAND_SLEEP_TIME_AFTER_ERROR)
                continue

            if response.status_code != 201:
                logger.error("Failed to get api token - %d", response.status_code)
                sleep(self.COMMAND_SLEEP_TIME_AFTER_ERROR)
                continue

            if not response.content:
                logger.error("No content was returned")
                sleep(self.COMMAND_SLEEP_TIME_AFTER_ERROR)
                continue

            try:
                token_info = json.loads(response.content)
            except Exception as e:
                logger.error("Failed to decode content - '%s': %s", response.content, e)
                sleep(self.COMMAND_SLEEP_TIME_AFTER_ERROR)
                continue

            api_token = token_info['token']

            # Get random painting
            try:
                headers = {
                    'X-XAPP-Token': api_token,
                }

                response = requests.get(self.COMMAND_RANDOM_PAINTING_URL,
                                        headers=headers)
            except Exception as e:
                logger.error("Failed to retrieve random painting - %s", e)
                sleep(self.COMMAND_SLEEP_TIME_AFTER_ERROR)
                continue

            if response.status_code != 200:
                logger.error("Failed to get random painting - %d", response.status_code)
                sleep(self.COMMAND_SLEEP_TIME_AFTER_ERROR)
                continue

            if not response.content:
                logger.error("No content was returned")
                sleep(self.COMMAND_SLEEP_TIME_AFTER_ERROR)
                continue

            try:
                random_painting = json.loads(response.content)
            except Exception as e:
                logger.error("Failed to decode content - '%s': %s", response.content, e)
                sleep(self.COMMAND_SLEEP_TIME_AFTER_ERROR)
                continue

            if not len(random_painting):
                logger.error("No random paintings were returned - '%s'", response.content)
                sleep(self.COMMAND_SLEEP_TIME_AFTER_ERROR)
                continue

            # Get artist
            try:
                headers = {
                    'X-XAPP-Token': api_token,
                }

                response = requests.get(random_painting['_links']['artists']['href'],
                                        headers=headers)
            except Exception as e:
                logger.error("Failed to retrieve random painting - %s", e)
                sleep(self.COMMAND_SLEEP_TIME_AFTER_ERROR)
                continue

            if response.status_code != 200:
                logger.error("Failed to get random painting - %d", response.status_code)
                sleep(self.COMMAND_SLEEP_TIME_AFTER_ERROR)
                continue

            if not response.content:
                logger.error("No content was returned")
                sleep(self.COMMAND_SLEEP_TIME_AFTER_ERROR)
                continue

            try:
                artists = json.loads(response.content)['_embedded']['artists']
            except Exception as e:
                logger.error("Failed to decode content - '%s': %s", response.content, e)
                sleep(self.COMMAND_SLEEP_TIME_AFTER_ERROR)
                continue

            if not len(artists):
                logger.error("No artists were returned - '%s'", response.content)
                sleep(self.COMMAND_SLEEP_TIME_AFTER_ERROR)
                continue

            try:
                painting = Painting()

                assert 'id'    in random_painting and len(random_painting['id'])
                assert 'title' in random_painting and len(random_painting['title'])
                assert 'date'  in random_painting and len(random_painting['date'])

                image_link = random_painting['_links']['image']['href']

                assert len(image_link)
                assert 'image_versions' in random_painting
                assert 'large' in random_painting['image_versions']


                logger.info("Inserting painting - (%s, %s)", random_painting['title'], random_painting['id'])

                painting.artsy_id = random_painting['id']
                painting.title = random_painting['title']
                painting.date = random_painting['date']
                painting.image_link = image_link.replace('{image_version}', 'large')

                painting.artist = ""

                for i, artist in enumerate(artists, start=1):

                    assert 'name' in artist and len(artist['name'])

                    painting.artist += artist['name']
                
                    if i < len(artists):
                        painting.artist += ', '

                painting.save()

            except Exception as e:
                logger.error("Failed to create painting - %s", e)
                sleep(self.COMMAND_SLEEP_TIME_AFTER_ERROR)
                continue

            seconds_to_wait = self.seconds_until_tomorrow()

            logger.info("Successfully inserted painting. Checking again in %d seconds",
                        seconds_to_wait)

            sleep(seconds_to_wait)
