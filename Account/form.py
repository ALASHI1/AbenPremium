from django import forms


class Contact_form(forms.Form):
    """A form for the users to contact the admin"""

    name = forms.CharField(max_length=200)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(max_length=200)
