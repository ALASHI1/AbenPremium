from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


def welcome_mail(request,user):
    """This Function sends the welcome email to the user

    Args:
            user (object): the activated user object
    """
    # checks if the project is running on https or http
    scheme = "https" if settings.SECURE_PROXY_SSL_HEADER else "http"
    # send mail function
    send_mail(
        "Congrats On Premium",  # subject
        # the message
        strip_tags(
            render_to_string(
                "email/welcome.html",
                {"name": user, "scheme": scheme,
                 "site": get_current_site(request)},
            )
        ),
        settings.DEFAULT_FROM_EMAIL,  # from email
        [user.email],  # to email
        # the html message
        html_message=render_to_string(
            "email/welcome.html",
            {"name": user, "scheme": scheme,
             "site": get_current_site(request)},
        ),
    )


def cancel_mail(request):
    """This function sends the cancellation email to the user"""
    # checks if the project is running on https or http
    scheme = "https" if settings.SECURE_PROXY_SSL_HEADER else "http"
    send_mail(
        "Sorry To See You Go",  # subject
        # the message
        strip_tags(
            render_to_string(
                "email/cancel.html",
                {
                    "name": request.user,
                    "scheme": scheme,
                    "site": get_current_site(request),
                },
            )
        ),
        settings.DEFAULT_FROM_EMAIL,  # from email
        [request.user.email],  # to email
        # the html message
        html_message=render_to_string(
            "email/cancel.html",
            {"name": request.user, "scheme": scheme,
             "site": get_current_site(request)},
        ),
    )


def resub_mail(request):
    """This function sends the resubscription email to the user"""
    # checks if the project is running on https or http
    scheme = "https" if settings.SECURE_PROXY_SSL_HEADER else "http"
    send_mail(
        "Congrats On Premium",  # subject
        # the message
        strip_tags(
            render_to_string(
                "email/success.html",
                {
                    "name": request.user,
                    "scheme": scheme,
                    "site": get_current_site(request),
                },
            )
        ),
        settings.DEFAULT_FROM_EMAIL,  # from email
        [request.user.email],  # to email
        # the html message
        html_message=render_to_string(
            "email/success.html",
            {"name": request.user, "scheme": scheme,
             "site": get_current_site(request)},
        ),
    )
