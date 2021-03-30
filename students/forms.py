from django import forms
from django.forms import FileInput
from django.forms import ModelForm
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.admin import widgets
from django.forms import formset_factory
from crispy_forms.helper import FormHelper, Layout


import mimetypes

from .models import StudentDocument


class StudentDocumentForm(ModelForm):
	class Meta:
		model = StudentDocument
		fields = ['name','status']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['name'].widget.attrs['disabled'] = 'disabled'
		# self.fields['name'].widget.attrs['required'] = False
		# self.fields['status'].widget.attrs['required'] = False

		field_names = [field_name for field_name, _ in self.fields.items()]
		for field_name in field_names:
			field = self.fields.get(field_name)
			field.label = ''




document_objects= {
	'PASSPORT' : 'Passport',
	'SSC_CERTIFICATE' : 'SSC / O Levels Certificate',
	'SSC_TRANSCRIPT' : 'SSC / O Levels Transcript',
	'HSC_CERTIFICATE' : 'HSC / A Levels Certificate',
	'HSC_TRANSCRIPT' : 'HSC / A Levels Transcript',
	'DIPLOMA_CERTIFICATE' : 'Diploma Certificate',
	'DIPLOMA_TRANSCRIPT' : 'Diploma Transcript',
	'BACHELORS_CERTIFICATE' : 'Bachelors Certificate',
	'BACHELORS_Transcript' : 'Bachelors Transcript',
	'MASTERS_CERTIFICATE' : 'Masters Certificate',
	'MASTERS_TRANSCRIPT' : 'Masters Transcript',
	'LANGUAGE_PROFICIENCY_CERTIFICATE' : 'Language Proficiency Certificate',
	'SOP' : 'SOP / Letter of Motivation',
	'RECOMMENDATION_LETTER' : 'Recommendation Letter',
}
StudentDocumentFormSet = formset_factory(StudentDocumentForm,extra=0)


