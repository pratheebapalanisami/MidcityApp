from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import F
from django.shortcuts import render



from ..forms import ApplyEventForm
from ..models import Event, Volunteership


class HomeView(ListView):
    model = Event
    template_name = 'home.html'
    context_object_name = 'events'

    def get_queryset(self):
        return self.model.objects.all()[:6]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trendings'] = self.model.objects.filter(created_at__month=timezone.now().month)[:3]
        return context


class SearchView(ListView):
    model = Event
    template_name = 'events/search.html'
    context_object_name = 'events'

    def get_queryset(self):
        return self.model.objects.filter(location__contains=self.request.GET['location'],
                                         title__contains=self.request.GET['position'])


class EventListView(ListView):
    model = Event
    template_name = 'events/events.html'
    context_object_name = 'events'
    paginate_by = 5


class EventDetailsView(DetailView):
    model = Event
    template_name = 'events/details.html'
    context_object_name = 'event'
    pk_url_kwarg = 'id'

    def get_object(self, queryset=None):
        obj = super(EventDetailsView, self).get_object(queryset=queryset)
        if obj is None:
            raise Http404("Event doesn't exists")
        return obj

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            # redirect here
            raise Http404("Event doesn't exists")
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class ApplyEventView(CreateView):
    model = Volunteership
    form_class = ApplyEventForm
    slug_field = 'event_id'
    slug_url_kwarg = 'event_id'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.info(self.request, 'Successfully applied for the event!')
            return self.form_valid(form)
        else:
            return HttpResponseRedirect(reverse_lazy('events:home'))

    def get_success_url(self):
        return reverse_lazy('events:events-detail', kwargs={'id': self.kwargs['event_id']})


    def form_valid(self, form):
        # check if user already applied
        volunteership = Volunteership.objects.filter(user_id=self.request.user.id, event_id=self.kwargs['event_id'])
        if volunteership:
            messages.info(self.request, 'You have already signed up for this event')
            return HttpResponseRedirect(self.get_success_url())
        # save volunteership
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

def contactus(request):
    return render(request, 'events/contactus.html', {'events': contactus})

def aboutus(request):
    return render(request, 'events/aboutus.html', {'events': aboutus})
