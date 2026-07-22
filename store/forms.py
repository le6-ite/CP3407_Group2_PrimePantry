from django import forms
from django.contrib.auth.models import User

from .models import CustomerProfile


class CustomerProfileForm(forms.Form):
    full_name = forms.CharField(max_length=150, label="Full name")
    email = forms.EmailField(label="Email address")
    phone = forms.CharField(max_length=40, required=False)
    address = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
        help_text="Used to prefill delivery checkout.",
    )
    preferred_fulfilment = forms.ChoiceField(
        choices=CustomerProfile.FULFILMENT_CHOICES,
        label="Preferred fulfilment",
    )

    def __init__(self, *args, user, profile, **kwargs):
        self.user = user
        self.profile = profile
        if not args and "initial" not in kwargs:
            kwargs["initial"] = {
                "full_name": user.first_name,
                "email": user.email,
                "phone": profile.phone,
                "address": profile.address,
                "preferred_fulfilment": profile.preferred_fulfilment,
            }
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "account-input"

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(username=email).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self):
        self.user.first_name = self.cleaned_data["full_name"].strip()
        self.user.email = self.cleaned_data["email"]
        self.user.username = self.cleaned_data["email"]
        self.user.save(update_fields=["first_name", "email", "username"])

        self.profile.phone = self.cleaned_data["phone"].strip()
        self.profile.address = self.cleaned_data["address"].strip()
        self.profile.preferred_fulfilment = self.cleaned_data["preferred_fulfilment"]
        self.profile.save()
        return self.profile
