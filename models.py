from django.db import models

class Painting (models.Model):

    PAINTING_MAX_ARTSY_ID_LEN = 128
    PAINTING_MAX_TITLE_LEN    = 400
    PAINTING_MAX_ARTIST_LEN   = 400
    PAINTING_MAX_DATE_LEN     = 128
    PAINTING_MAX_LINK_LEN     = 400

    artsy_id = models.CharField(
        help_text='Artsy ID of artwork',
        max_length=PAINTING_MAX_ARTSY_ID_LEN,
        unique=True,
        db_index=True)

    title = models.CharField(
        help_text='Title of painting',
        max_length=PAINTING_MAX_TITLE_LEN,
        db_index=True)

    artist = models.CharField(
        help_text='Artist of painting',
        max_length=PAINTING_MAX_ARTIST_LEN,
        db_index=True)

    date_selected = models.DateField(
        help_text='Date of when painting was selected',
        auto_now_add=True,
        unique=True,
        db_index=True)

    date = models.CharField(
        help_text='Date of painting',
        max_length=PAINTING_MAX_DATE_LEN,
        db_index=True)

    image_link = models.CharField(
        help_text='Link to image of painting',
        max_length=PAINTING_MAX_LINK_LEN,
        db_index=True)
