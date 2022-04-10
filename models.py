from django.db import models

class Painting (models.Model):

    PAINTING_MAX_ARTSY_ID_LEN = 128

    artsy_id = models.CharField(
        help_text='Artsy ID of artwork',
        max_length=PAINTING_MAX_ARTSY_ID_LEN,
        db_index=True)

    date_selected = models.DateField(
        help_text='Date of when painting was selected',
        auto_now_add=True,
        unique=True,
        db_index=True)
