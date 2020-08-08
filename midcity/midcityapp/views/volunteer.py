from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, CreateView, ListView

from accounts.forms import VolunteerProfileUpdateForm
from accounts.models import User
from midcityapp.models import Event, Volunteership
from midcityapp.decorators import user_is_volunteer


class EditProfileView(UpdateView):
    model = User
    form_class = VolunteerProfileUpdateForm
    context_object_name = 'volunteer'
    template_name = 'events/volunteer/edit-profile.html'
    success_url = reverse_lazy('accounts:organization-profile-update')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_volunteer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            raise Http404("User doesn't exists")
        # context = self.get_context_data(object=self.object)
        return self.render_to_response(self.get_context_data())

    def get_object(self, queryset=None):
        obj = self.request.user
        print(obj)
        if obj is None:
            raise Http404("Event doesn't exists")
        return obj



class VolunteershipPerUserView(ListView):
    model = Volunteership
    template_name = 'events/volunteer/my-volunteerships.html'
    context_object_name = 'myvolunteerships'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_volunteer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return Volunteership.objects.filter(user_id=self.kwargs['user_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = Event.objects.get(id=self.kwargs['user_id'])
        return context
