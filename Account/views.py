import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.dispatch import receiver
from django.shortcuts import render
from django.template.loader import render_to_string
from django_registration.backends.activation.views import RegistrationView
from django_registration.signals import user_activated

from Account.form import Contact_form
from Account.models import StripeCustomer
from Account.utils import welcome_mail

stripe.api_key = (
    settings.STRIPE_SECRET_KEY
)  # assigns the stripe secret key to the stripe object


class MyRegistrationView(RegistrationView):
    """Extend the default registration view to send an activation email

    Args:
        RegistrationView (class): gets the username
        and creates the activation key
    """

    email_body_template = "email/activation_email_body.html"
    email_subject_template = "email/activation_email_subject.txt"

    def send_activation_email(self, user):
        """
        Send the activation email. The activation key is the username,
        signed using TimestampSigner.

        """
        activation_key = self.get_activation_key(user)
        context = self.get_email_context(activation_key)
        context["user"] = user
        subject = render_to_string(
            template_name=self.email_subject_template,
            context=context,
            request=self.request,
        )
        # Force subject to a single line to avoid header-injection
        # issues.
        subject = "".join(subject.splitlines())
        # rending the email body
        html_message = render_to_string(
            template_name=self.email_body_template,
            context=context,
            request=self.request,
        )
        message = EmailMessage(
            subject, html_message, settings.DEFAULT_FROM_EMAIL, [user.email]
        )
        message.content_subtype = (
            "html"  # this is required because there is no plain text message
        )
        message.send()


def home(request):
    """This is the home page of the website

    Returns:
        template: A bootstrap template of the homepage
    """
    # contact form
    if request.method == "POST":
        # requesting the details from the form
        form = Contact_form(request.POST)
        if form.is_valid():
            messages.success(
                request, "successfully sent"
            )  # if the form is valid then the message is sent
        else:
            messages.error(
                request, "Error sending contact"
            )  # if the form is not valid then the message is not sent
    else:
        form = Contact_form()  # displays the form when the page is loaded
    return render(request, "index.html", {"form": form})


@login_required  # ensures that the user is logged in
def dashboard(request):
    """This is the dashboard of the website
    Returns:
        template: A bootstrap template of the Dashboard
    """
    username = request.user.username
    try:
        # Retrieve the subscription using the StripeCustomer model
        stripe_customer = StripeCustomer.objects.get(
            user=request.user
        )  # gets the stripe customer object for the current user
        subscription = stripe.Subscription.retrieve(
            stripe_customer.stripeSubscriptionId
        )  # gets the current subscription for the logged in user
        return render(
            request,
            "dash.html",
            {
                "stripe_customer": stripe_customer,
                "subscription": subscription,
                "username": username,
            },
        )
    except Exception:  # checks if there is an error
        return render(request, "dash.html", {"username": username})


@login_required  # ensures that the user is logged in
def table(request):
    """This is a tab on the dashboard that shows a table of the transactions
    Returns:
        template: A bootstrap template of the Dashboard Table
    """
    username = request.user.username
    try:
        # Retrieve the subscription using the StripeCustomer model
        stripe_customer = StripeCustomer.objects.get(
            user=request.user
        )  # gets the stripe customer object for the current user
        subscription = stripe.Subscription.retrieve(
            stripe_customer.stripeSubscriptionId
        )  # gets the current subscription for the logged in user
        return render(
            request,
            "basic-table.html",
            {
                "stripe_customer": stripe_customer,
                "subscription": subscription,
                "username": username,
            },
        )
    except Exception:  # checks if there is an error
        return render(request, "basic-table.html", {})


@receiver(user_activated)  # signal that is sent when a user is activated
def stripe_signup(request, user, **kwargs):
    """This is the function that is called when a user is activated

    Args:
        user (object): this allow the function to get the user object
    """
    customer = stripe.Customer.create(
        email=user.email
    )  # creates a customer object for the user
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
    # creates a StripeCustomer object to saveinformation to the database
    StripeCustomer.objects.create(
        user=user, stripeCustomerId=customer["id"], stripeSubscriptionId=sub.id
    )
    # sends a welcome email to the user after they are activated
    welcome_mail(request,user)
