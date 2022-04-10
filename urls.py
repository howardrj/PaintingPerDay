from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter

from painting_per_day import views

router = SimpleRouter()

router.register(r'^api/paintings', views.PaintingViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^painting_per_day/$', views.painting_per_day_main),
]
