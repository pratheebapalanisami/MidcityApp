from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView
from django.shortcuts import render, get_object_or_404

from midcityapp.decorators import user_is_organization
from midcityapp.forms import CreateEventForm, VolunteershipForm
from midcityapp.models import Event, Volunteership
from accounts.models import User


class DashboardView(ListView):
    model = Event
    template_name = 'events/organization/dashboard.html'
    context_object_name = 'events'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_organization)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id)


class VolunteershipPerEventView(ListView):
    model = Volunteership
    template_name = 'events/organization/volunteerships.html'
    context_object_name = 'volunteerships'
    paginate_by = 5

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_organization)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return Volunteership.objects.filter(event_id=self.kwargs['event_id']).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = Event.objects.get(id=self.kwargs['event_id'])
        return context


class EventCreateView(CreateView):
    model = None
    object = None
    template_name = 'events/create.html'
    form_class = CreateEventForm
    extra_context = {
        'title': 'Post New Event'
    }
    success_url = reverse_lazy('events:organization-dashboard')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('accounts:login')
        if self.request.user.is_authenticated and self.request.user.role != 'organization':
            return reverse_lazy('accounts:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(EventCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        # self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class VolunteershipsListView(ListView):
    model = Volunteership
    template_name = 'events/organization/all-volunteerships.html'
    context_object_name = 'volunteerships'

    def get_queryset(self):
        # events = Event.objects.filter(user_id=self.request.user.id)
        return self.model.objects.filter(event__user_id=self.request.user.id)


def attendance(request, pk):
    volunteership = get_object_or_404(Volunteership, pk=pk)
    if request.method == "POST":
        # update attendance
        form = VolunteershipForm(request.POST, instance=volunteership)
        if form.is_valid():
            volunteership = form.save(commit=False)
            volunteership.save()
            volunteerships = Volunteership.objects.filter()
            return render(request, 'events/organization/all-volunteerships.html',
                          {'volunteerships': volunteerships})
    else:
        # edit attendance
        form = VolunteershipForm(instance=volunteership)
    return render(request, 'events/organization/attendance.html', {'form': form})


@login_required(login_url=reverse_lazy('accounts:login'))
def filled(request, event_id=None):
    event = Event.objects.get(user_id=request.user.id, id=event_id)
    event.filled = True
    event.save()
    return HttpResponseRedirect(reverse_lazy('events:organization-dashboard'))
