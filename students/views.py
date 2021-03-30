from django.shortcuts import render, redirect,get_object_or_404,HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.db.models import Prefetch
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View, generic
from django.contrib.auth import get_user_model





from accounts.mixins import SuperAdminRequiredMixin

from branch.models import Branch
from lead_management.models import Lead,Event,TaskAssign
from students.models import Student,StudentDocument
from students.forms import StudentDocumentForm,StudentDocumentFormSet,document_objects


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
	    # context['document_form_set'] = StudentDocumentFormSet(initial=[{'name': x} for x in document_objects.values()])
	    context["document_objects"] = document_objects
	    return context



class AddStudentDocumentView(LoginRequiredMixin,View):
	def post(self,request,*args,**kwargs):
		student_id = self.kwargs.get('student_id')
		student_obj = get_object_or_404(Student,id=student_id)

		document_list = request.POST.getlist('name')
		document_status_list = request.POST.getlist('status')


		# aList = [StudentDocument(student=student_obj,name=document,status=document_status_list[index]) for index,document in enumerate(document_list)]
		# StudentDocument.objects.bulk_create(aList)

		for index,document in enumerate(document_list):
			if document != '':
				print(document)
				StudentDocument.objects.update_or_create(student=student_obj,name__icontains=document,defaults={'status' : document_status_list[index]})

		return redirect("students:student_detail",student_id)




