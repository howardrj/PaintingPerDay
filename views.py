from painting_per_day.models import Painting
from rest_framework import viewsets
from django.shortcuts import render

from painting_per_day.serializers import PaintingSerializer

class PaintingViewSet (viewsets.ModelViewSet):

    serializer_class = PaintingSerializer
    queryset         = Painting.objects.all()

def painting_per_day_main (request):

    context_dict = {}

    # Get paintings in reverse order
    paintings = Painting.objects.order_by('-id')

    if len(paintings):
        context_dict['painting'] = paintings[0]

    return render(request, 'painting_of_the_day.html', context_dict)
