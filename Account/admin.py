from django.contrib import admin

# Register your models here.
from Account.models import StripeCustomer

# register the stripe customer model on the admin page
admin.site.register(StripeCustomer)
