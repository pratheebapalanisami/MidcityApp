from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import F

from accounts.models import User

# EVENT_TYPE = (
#     ('1', "Full time"),
#     ('2', "Part time"),
#     ('3', "Internship"),
# )


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    description = models.TextField()
    location = models.CharField(max_length=150)
    # type = models.CharField(choices=EVENT_TYPE, max_length=10)
    category = models.CharField(max_length=100)
    last_date = models.DateTimeField()
    company_name = models.CharField(max_length=100)
    company_description = models.CharField(max_length=300)
    website = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    filled = models.BooleanField(default=False)
    volunteers_required = models.IntegerField(default=1, validators=[MaxValueValidator(5),MinValueValidator(1)], blank=True)

    def __str__(self):
        return self.title

    # def volunteerupdate(self):
    #     self.volunteers_required -= 1

class Volunteership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='myvolunteerships')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='volunteerships')
    attendance = models.BooleanField(default=False)
    hours = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.get_full_name()



