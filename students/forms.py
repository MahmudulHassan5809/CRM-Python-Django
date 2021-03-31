from django import forms
from django.forms import FileInput
from django.forms import ModelForm
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.admin import widgets
from django.forms import formset_factory
from crispy_forms.helper import FormHelper, Layout
from django.forms.models import inlineformset_factory

import mimetypes

from .models import StudentDocument,StudentCredentials,StudentApplicationStatus,Student


STUDENT_DOCUMENT_INTITAL_DATA = """<ol>
					<li><b>Passport:</b>  Not Received</li>
					<li><b>SSC Certificate:</b>  Not Received</li>
					<li><b>SSC Transcript:</b>  Not Received</li>
					<li><b>HSC Certificate:</b>  Not Received</li>
					<li><b>HSC Transcript:</b>  Not Received</li>
					<li><b>Bachelor Certificate:</b>  Not Received</li>
					<li><b>Bachelor Transcript:</b>  Not Received</li>
					<li><b>IELTS:</b>  Not Received</li>
					<li><b>SOP:</b>  Not Received</li>
					<li><b>Job Experience:</b>  Not Received</li>
					<li><b>Letter of Recommendation (Academic):</b>  Not Received</li>
					<li><b>Letter of Recommendation (Professional):</b>  Not Received</li>
				</ol>"""


class StudentDocumentForm(ModelForm):
	class Meta:
		model = StudentDocument
		fields = ['documents']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		field_names = [field_name for field_name, _ in self.fields.items()]
		for field_name in field_names:
			field = self.fields.get(field_name)
			field.label = ''


class StudentCredentialsForm(ModelForm):
	class Meta:
		model = StudentCredentials
		fields = ['credentials']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		field_names = [field_name for field_name, _ in self.fields.items()]
		for field_name in field_names:
			field = self.fields.get(field_name)
			field.label = ''




class StudentApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = StudentApplicationStatus
        fields = '__all__'


ApplicationStatusFormSet = inlineformset_factory(
    Student, StudentApplicationStatus, form=StudentApplicationStatusForm, extra=1)
