from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register('events', EventViewSet, base_name='events')

urlpatterns = [
    path('search/', SearchApiView.as_view()),
    path('apply-event/<int:event_id>', ApplyEventApiView.as_view())
]

urlpatterns += router.urls
