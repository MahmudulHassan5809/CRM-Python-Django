from django import forms
from django.forms import FileInput
from django.forms import ModelForm
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.admin import widgets

import mimetypes

from .models import Lead,Event,TaskAssign


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


class BulkLeadCreateForm(forms.Form):
	event = forms.ModelChoiceField(required=True,queryset=Event.objects.filter(active=True))
	file = forms.FileField(label='Select a file')


	def clean_file(self):
		excel_file = self.cleaned_data.get('file')
		content_type, charset = mimetypes.guess_type(excel_file.name)
		extension = str(content_type).split('.')[-1]

		if extension != 'sheet':
			raise forms.ValidationError(f'Your file formate {extension} is not valid. Valid excel extension is xlsx.')
		return excel_file



	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		field_names = [field_name for field_name, _ in self.fields.items()]
		for field_name in field_names:
			field = self.fields.get(field_name)
			field.widget.attrs.update({'placeholder': field.label})




class TaskAssignForm(ModelForm):
	class Meta:
		model = TaskAssign
		fields = ['branch','assignee']



class UpdateLeadForm(forms.ModelForm):
	note = forms.CharField(required=True,widget=forms.Textarea(attrs={'rows': 1, 'cols': 40}))
	country_of_interest = forms.CharField(required=True,widget=forms.Textarea(attrs={'rows': 1, 'cols': 40}))
	class Meta:
		model = Lead
		exclude = ["event","created_by","created_at",'assigned']


class LeadFilterByStatusForm(forms.Form):
	LEAD_STATUS_CHOICE = [
        ('Not Available', (
            ('PHONE_OFF', 'Phone Off'),
            ('NO ANSWER', 'No Answer'),
            ('CALL_FORWARDED', 'Call Forwarded'),
            ('INCORREET_NUMBER', 'Incorrect Number'),
            ('OTHER', 'Other'),
        )
        ),
        ('Video', (
                ('vhs', 'VHS Tape'),
                ('dvd', 'DVD'),
            )
        ),
        ('NEW', 'New'),
    ]
	status = forms.ChoiceField(choices=LEAD_STATUS_CHOICE,required=True,label=False)
