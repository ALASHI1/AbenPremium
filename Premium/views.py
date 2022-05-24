import stripe
from Account.models import StripeCustomer
from Account.utils import cancel_mail, resub_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required  # ensures that the user is logged in
def cancel_subscription(request):
    """This function cancels the subscription of the user
    Returns:
        template: A bootstrap template of the dashboard
        without the premium features
    """
    user_sub = StripeCustomer.objects.get(
        user=request.user
    )  # gets the user's subscription details from the database
    stripe.Subscription.delete(
        user_sub.stripeSubscriptionId
    )  # cancels the subscription from the stripe account
    sub = stripe.Subscription.retrieve(
        str(user_sub.stripeSubscriptionId)
    )  # gets the subscription details from the stripe account
    # checks if the subscription status if cancelled
    if sub.status == "canceled":
        # success message
        messages.success(request, "Your subscription has been canceled.")
        # sets the subscription id to none
        user_sub.stripeSubscriptionId = None
        user_sub.save()
        cancel_mail(request)  # sends a cancellation email to the user
        return redirect("/dashboard")  # redirects to the dashboard
    else:
        messages.error(
            request, "Your subscription could not be canceled."
        )  # error message
    return redirect("/dashboard")


@login_required  # ensures that the user is logged in
def resub(request):
    """This function resubscribes the user to the premium features
    Returns:
        template: A bootstrap template of the dashboard
        with the premium features
    """
    customer = stripe.Customer.create(
        email=request.user.email
    )  # recreates a customer object for the user
    # Modifies the stripe Customer object to add values
    stripe.Customer.modify(
        customer["id"],
        source="tok_visa",
    )
    # creates a Subscription for the user with a free 7 days trial
    sub = stripe.Subscription.create(
        customer=customer,
        items=[
            {
                "price": settings.STRIPE_PRICE_ID,
            },
        ],
        trial_period_days=7,
    )
    # gets the user's subscription details from the database
    re_subscriber = StripeCustomer.objects.get(user=request.user)
    re_subscriber.stripeSubscriptionId = (
        sub.id
    )  # sets the subscription id to the new subscription id
    re_subscriber.save()
    resub_mail(request)  # sends a resubscription email to the user
    return redirect("/dashboard")  # redirects to the dashboard
