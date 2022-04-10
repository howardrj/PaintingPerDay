from painting_per_day.models import Painting
from rest_framework import serializers

class PaintingSerializer (serializers.ModelSerializer):

    class Meta:
        model = Painting
        fields = '__all__'

        # Set all fields to read only
        read_only_fields = [f.name for f in Painting._meta.get_fields()]
