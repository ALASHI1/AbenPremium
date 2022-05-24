from django.db import models
from django.contrib.auth.models import User


class StripeCustomer(models.Model):
    """A model to store the stripe
    customer and subscription ids for each user
    """

    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    stripeCustomerId = models.CharField(max_length=255)
    stripeSubscriptionId = models.CharField(max_length=255,
                                            null=True, blank=True)

    def __str__(self):
        """A string representation of the StripeCustomer model

        Returns:
            string: the user's username
        """
        return self.user.username
