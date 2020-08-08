from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from midcityapp.views import EditProfileView
from .views import *

app_name = "accounts"

urlpatterns = [
    path('volunteer/register', RegisterVolunteerView.as_view(), name='volunteer-register'),
    path('organization/register', RegisterOrganizationView.as_view(), name='organization-register'),
    path('volunteer/profile/update', EditProfileView.as_view(), name='organization-profile-update'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('login', LoginView.as_view(), name='login'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
