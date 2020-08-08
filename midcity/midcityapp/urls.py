from django.urls import path, include

from .views import *
from . import views

app_name = "events"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search', SearchView.as_view(), name='searh'),
    path('contactus', views.contactus, name='contactus'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('organization/dashboard', include([
        path('', DashboardView.as_view(), name='organization-dashboard'),
        path('all-volunteerships', VolunteershipsListView.as_view(), name='organization-all-volunteerships'),
        path('volunteerships/<int:event_id>', VolunteershipPerEventView.as_view(), name='organization-dashboard-volunteerships'),
        path('mark-filled/<int:event_id>', filled, name='event-mark-filled'),
        path('attendance/<pk>/edit/', views.attendance, name='attendance'),
    ])),
    path('apply-event/<int:event_id>', ApplyEventView.as_view(), name='apply-event'),
    path('volunteerships/<int:user_id>', VolunteershipPerUserView.as_view(), name='myvolunteerships'),
    path('events', EventListView.as_view(), name='events'),
    path('events/<int:id>', EventDetailsView.as_view(), name='events-detail'),
    path('organization/events/create', EventCreateView.as_view(), name='organization-events-create'),

]
