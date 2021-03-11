from django import forms
from django.forms import FileInput
from django.forms import ModelForm

from django.forms.widgets import PasswordInput, TextInput

from .models import Branch


class BranchCreateForm(ModelForm):
    class Meta:
        model = Branch
        fields = '__all__'

