from django.shortcuts import render, redirect,get_object_or_404,HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.db.models import Prefetch
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View, generic
from django.contrib.auth import get_user_model



from django.db import transaction

from accounts.mixins import SuperAdminRequiredMixin

from branch.models import Branch
from lead_management.models import Lead,Event,TaskAssign
from students.models import Student,StudentDocument,StudentCredentials
from students.forms import StudentDocumentForm,StudentCredentialsForm,ApplicationStatusFormSet,STUDENT_DOCUMENT_INTITAL_DATA


# Create your views here.
class StudentListView(LoginRequiredMixin,generic.ListView):
	model = Student
	template_name = 'students/student_list.html'
	paginate_by = 10
	context_object_name = 'student_list'

	def get_query_set(self,**kwargs):
		qs = super().get_query_set()

		if self.request.user.user_type != 'SUPER_ADMIN':
			qs = qs.filter_by_assignee(self.request.id)

		return qs

	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['title'] = "Student List"
	    return context



class StudentDetailView(LoginRequiredMixin,generic.DetailView):
	model = Student
	template_name = 'students/student_detail.html'
	context_object_name = 'student_obj'



	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['title'] = "Student Details"
	    context['application_status_form'] = ApplicationStatusFormSet(instance=self.object)

	    if hasattr(self.object,'documents'):
	    	context["document_form"] = StudentDocumentForm(initial={'documents' : self.object.documents.documents})
	    else:
	    	context["document_form"] = StudentDocumentForm(initial={'documents' : STUDENT_DOCUMENT_INTITAL_DATA})

	    if hasattr(self.object,'credentials'):
	    	context["credentials_form"] = StudentCredentialsForm(initial={'credentials' : self.object.credentials.credentials})
	    else:
	    	context["credentials_form"] = StudentCredentialsForm()



	    return context



class AddStudentDocumentView(LoginRequiredMixin,View):
	def post(self,request,*args,**kwargs):
		student_id = self.kwargs.get('student_id')
		student_obj = get_object_or_404(Student,id=student_id)

		documents = request.POST.get('documents')

		if hasattr(student_obj,'documents'):
			student_obj.documents.documents = document
			student_obj.documents.save()
		else:
			StudentDocument.objects.create(student=student_obj,documents=documents)


		return redirect("students:student_detail",student_id)





class AddStudentCredentialsView(LoginRequiredMixin,View):
	def post(self,request,*args,**kwargs):
		student_id = self.kwargs.get('student_id')
		student_obj = get_object_or_404(Student,id=student_id)

		credentials = request.POST.get('credentials')

		if hasattr(student_obj,'credentials'):
			student_obj.credentials.credentials = credentials
			student_obj.credentials.save()
		else:
			StudentCredentials.objects.create(student=student_obj,credentials=credentials)


		return redirect("students:student_detail",student_id)


class AddStudentStatusView(LoginRequiredMixin,View):
	def post(self,request,*args,**kwargs):
		student_id = self.kwargs.get('student_id')
		student_obj = get_object_or_404(Student,id=student_id)
		form = ApplicationStatusFormSet(self.request.POST, instance=student_obj)

		if form.is_valid():
			with transaction.atomic():
				form.instance = student_obj
				form.save()
				return redirect('students:student_detail', student_id)
		else:
			print(form.errors)
			return self.render_to_response(self.get_context_data(form=form))
		return super().form_valid(form)

