from crispy_forms.helper import FormHelper
from django.db.models.base import Model
from django.forms import ModelForm

from django.forms import ModelForm, Textarea, HiddenInput,DateInput
from .models import Contact_us

from django import forms
from.models import(Contact_us)


class ContactForm(ModelForm):

    class Meta:
        model = Contact_us

        fields = fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()