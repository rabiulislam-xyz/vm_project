from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # USER_TYPE_CHOICES = (
    #     ('OM', 'Operation Manager'),
    #     ('VM', 'Vehicle Manager'),
    #     ('BM', 'Branch Manager'),
    #     ('DR', 'Driver'),
    #     ('HE', 'Helper'),
    # )

    # user_type  = models.CharField(max_length=2, choices=USER_TYPE_CHOICES)
    name       = models.CharField(max_length=225)
    phone      = models.IntegerField(blank=True, null=True)
    nid        = models.IntegerField(blank=True, null=True)
    address    = models.CharField(max_length=511, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def role(self):
        return ', '.join([group.name for group in self.groups.all()])
    role.short_description = 'Role'

    def __str__(self):
        return self.username

