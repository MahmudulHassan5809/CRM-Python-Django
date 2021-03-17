from django import forms
from django.forms import FileInput
from django.forms import ModelForm
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.admin import widgets

from .models import Lead,Event


class EventCreateForm(ModelForm):
	class Meta:
		model = Event 
		exclude = ('active',)
		js = ('admin/js/vendor/jquery/jquery.min.js', 'admin/js/jquery.init.js')
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['event_date'].widget = AdminDateWidget()

		field_names = [field_name for field_name, _ in self.fields.items()]
		for field_name in field_names:
			field = self.fields.get(field_name)
			field.widget.attrs.update({'placeholder': field.label})


class LeadCreateForm(ModelForm):
    country_of_interest = forms.CharField(required=True)

    class Meta:
        model = Lead
        exclude = ['created_by',]
