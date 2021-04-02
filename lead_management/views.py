from django.shortcuts import render, redirect,get_object_or_404,HttpResponse
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.db.models import Count
from django.db.models import Prefetch
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View, generic
from django.contrib.auth import get_user_model

import os
import tempfile
import xlrd

import pandas as pd
import mimetypes
import json
from django_tables2 import SingleTableView,LazyPaginator


from accounts.mixins import SuperAdminRequiredMixin


from branch.models import Branch
from .models import Lead,Event,TaskAssign
from students.models import Student
from django.views.generic.edit import FormMixin
from .forms import LeadCreateForm,EventCreateForm,BulkLeadCreateForm,TaskAssignForm,UpdateLeadForm,LeadFilterByStatusForm
from .tables import TaskAssignTable

# Create your views here.


User = get_user_model()

class CreateEvent(SuccessMessageMixin,LoginRequiredMixin,SuperAdminRequiredMixin,generic.CreateView):
	model = Event
	form_class = EventCreateForm
	template_name = "lead_management/event/super_user/create_event.html"
	success_message = "Event created successfully"

	def get_success_url(self,**kwargs):
		return reverse("lead_management:event_list")


	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['title'] = "Create Event"
	    return context



class EventListView(SuccessMessageMixin,LoginRequiredMixin,generic.ListView):
	model = Event
	contect_object_name = "event_list"
	template_name = "lead_management/event/super_user/event_list.html"
	paginate_by = 10

	def get_queryset(self,**kwargs):
		qs = super().get_queryset()

		query = self.request.GET.get('query',None)
		if query:
			qs = qs.filter_by_query(query)

		return qs



	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['title'] = "Create List"
	    return context



class CreateSingleLead(SuccessMessageMixin,LoginRequiredMixin,SuperAdminRequiredMixin,generic.CreateView):
	model = Lead
	form_class = LeadCreateForm
	template_name = "lead_management/lead/super_user/create_lead.html"
	success_message = "Lead created successfully"


	def form_valid(self,form):
		country_of_interest = form.cleaned_data.get('country_of_interest')
		country_of_interest = form.cleaned_data.get('country_of_interest')
		country_of_interest =  country_of_interest.rstrip(',')
		obj = form.save(commit=False)
		obj.created_by = self.request.user
		obj.save()
		return redirect('lead_management:lead_list',obj.event_id)


	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['title'] = "Create Lead"
	    return context




class CreateBulkLeadView(LoginRequiredMixin,SuperAdminRequiredMixin,generic.FormView):
	form_class = BulkLeadCreateForm
	template_name = "lead_management/lead/super_user/create_bulk_lead.html"
	success_message = "Lead created successfully"

	def form_valid(self,form):
		event = form.cleaned_data.get("event")
		excel_file = self.request.FILES['file']
		content_type, charset = mimetypes.guess_type(excel_file.name)
		extension = str(content_type).split('.')[-1]

		df = pd.read_excel(excel_file,dtype=str)
		df.fillna('', inplace=True)
		df.columns = df.columns.str.lower()
		df.columns = df.columns.str.replace(' ','_')
		df.columns = df.columns.str.replace(r"\(.*\)","")
		df.columns = df.columns.str.rstrip('_')
		df.drop(df.filter(regex="unnamed"),axis=1, inplace=True)
		df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%d')
		df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d')

		data = df.to_json(orient='records')

		data = json.loads(data)

		for row in data:
			created_at = row['timestamp']
			name = row['name']
			email_address = row['email_address']
			phone_number = row['phone_number']
			present_address = row['present_address']
			country_of_interest = row['country_of_interest']
			last_completed_education = row['last_completed_education']
			ielts_score = row['ielts_score']
			remarks = row['remarks']

			Lead.objects.get_or_create(
				event = event,
				email = email_address,
				phone_number = phone_number,
				defaults={
					'created_by' : self.request.user,
					'name' : name,
					'present_address' : present_address,
					'country_of_interest' : country_of_interest,
					'last_completed_education' : last_completed_education,
					'ielts' : ielts_score,
					'remarks' : remarks,
					'created_at' : created_at
				}
			)

		return redirect('lead_management:lead_list',event.id)



	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['title'] = "Create Lead"
	    return context


class LeadListView(LoginRequiredMixin,SuperAdminRequiredMixin,generic.ListView):
	model = Lead
	contect_object_name = "lead_list"
	template_name = "lead_management/lead/super_user/lead_list.html"
	paginate_by = 10

	def get_queryset(self,**kwargs):
		qs = super().get_queryset()

		event_id = self.kwargs.get('event_id',None)
		if event_id:
			qs = qs.filter_by_event(event_id)


		query = self.request.GET.get('query',None)
		if query:
			qs = qs.filter_query(query)

		status = self.request.GET.get('status',None)
		if status:
			qs = qs.filter_by_status(status)

		return qs


	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['title'] = "Lead List"
	    context["event_id"] = self.kwargs.get('event_id',None)
	    context["form"] = LeadFilterByStatusForm()
	    return context


class LeadManagementView(LoginRequiredMixin,SuperAdminRequiredMixin,SingleTableView):
	def get(self,request,*args,**kwargs):
		event_id = self.kwargs.get('event_id',None)
		lead_type = self.kwargs.get('type',None)

		if lead_type == 'unassigned':
			qs = Lead.objects.filter_by_event(event_id).filter_by_is_assigned(False).select_related("lead_task__assignee")
		elif lead_type == 'assigned':
			qs = Lead.objects.filter_by_event(event_id).filter_by_is_assigned(True).select_related("lead_task__assignee")
		else:
			qs = Lead.objects.filter_by_event(event_id).select_related("lead_task__assignee")


		table = TaskAssignTable(qs)
		table.paginate(paginator_class = LazyPaginator,page=request.GET.get("page", 1), per_page=25)
		task_assign_form = TaskAssignForm()
		context = {
			'table' : table,
			'title' : 'Lead Management',
			'event_id' : event_id,
			'lead_type' : lead_type,
			'task_assign_form' : task_assign_form,
			'unassigned_count' : Lead.objects.filter_by_event(event_id).filter_by_is_assigned(False).count(),
			'assigned_count' : Lead.objects.filter_by_event(event_id).filter_by_is_assigned(True).count()
		}

		return render(request,'lead_management/lead/super_user/lead_management.html',context)

	def post(self,request,*args,**kwargs):
		event_id = self.kwargs.get('event_id',None)
		lead_type = self.kwargs.get('type',None)
		pks  = request.POST.getlist("selection",None)
		branch_id = request.POST.get("branch",None)
		assignee_id = request.POST.get("assignee",None)


		print(event_id,lead_type,pks,branch_id,type(assignee_id))


		event_obj = None
		assignee_obj = None
		branch_obj = None
		if event_id != '':
			event_obj = get_object_or_404(Event,id=event_id)
		if assignee_id:
			assignee_obj = get_object_or_404(User,id=assignee_id)
		if branch_id:
			branch_obj = get_object_or_404(Branch,id=branch_id)


		if len(pks) > 0:
			if lead_type == "unassigned" and event_obj and assignee_obj and branch_obj: # Lead type unassigned that means we need to assigned these unassigned task to some one
				for pk in pks:
					TaskAssign.objects.create(lead_id=pk,branch_id=branch_id,assignee_id=assignee_id,event_id=event_id)

				Lead.objects.filter(id__in=pks).update(assigned=True)
				message = f"{len(pks)} Leads of {event_obj.name} is Assigned to {assignee_obj.username.upper()} of {branch_obj.branch_name} Branch."

			elif lead_type == "assigned" and event_obj and assignee_obj and branch_obj: # Lead type assigned and new branch and new assignee added that means we need to reassigned these assigned task to new one
				TaskAssign.objects.filter(lead_id__in=pks).update(branch_id=branch_id,assignee_id=assignee_id)
				message = f"{len(pks)} Leads of {event_obj.name} is ResignedAssigned to {assignee_obj.username.upper()} of {branch_obj.branch_name} Branch."

			elif lead_type == 'remove_task' and event_obj:
				TaskAssign.objects.filter(lead_id__in=pks).delete()
				Lead.objects.filter(id__in=pks).update(assigned=False)
				message = f"{len(pks)} Leads of {event_obj.name} is removed from tasklist"
			else:
				print("Here")
			status = 200
		else:
			message = f"Please Select Some Students And Select Branch & User"
			status = 400

		return HttpResponse(json.dumps(message),content_type="application/json", status=status)





class UserEventListView(LoginRequiredMixin,View):
	def get(self,request,*args,**kwargs):
		event_id_list = list(TaskAssign.objects.filter_by_assignee(request.user.id).values_list("event__id",flat=True).distinct())
		event_list = Event.objects.filter(id__in=event_id_list)
		query = self.request.GET.get('query',None)
		if query:
			event_list = event_list.filter_by_query(query)

		status = self.request.GET.get('status',None)

		context = {
			'title' : 'User Event List',
			'event_list' : event_list,
			'form' : LeadFilterByStatusForm()
		}
		return render(request,'lead_management/event/user/event_list.html',context)


class UserLeadListView(LoginRequiredMixin,generic.ListView):
	model = Lead
	template_name = 'lead_management/lead/user/lead_list.html'
	context_object_name = 'lead_list'
	paginate_by = 10

	def get_queryset(self,**kwargs):
		qs = super().get_queryset()
		event_id = self.kwargs.get('event_id',None)

		if event_id:
			lead_id_list = list(TaskAssign.objects.filter_by_event(event_id).filter_by_assignee(self.request.user.id).values_list('lead__id',flat=True))
			qs = qs.filter(id__in=lead_id_list)

			query = self.request.GET.get('query',None)
			if query:
				qs = qs.filter_query(query)

			status = self.request.GET.get('status',None)
			if status:
				qs = qs.filter_by_status(status)
		else:
			qs = []

		return qs



	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['title'] = "Lead List"
	    context["event_id"] = self.kwargs.get('event_id',None)
	    context["form"] = LeadFilterByStatusForm()
	    return context



class LeadDetailsView(SuccessMessageMixin,LoginRequiredMixin,generic.UpdateView):
	model = Lead
	form_class = UpdateLeadForm
	context_object_name = 'lead_obj'
	success_message = "Information updated successfully..."
	template_name = 'lead_management/lead/user/lead_details.html'

	def get_success_url(self,**kwargs):
		if self.request.POST.get('save_continue',None):
			check_next_lead = TaskAssign.objects.filter(lead__id__gt=self.object.id,assignee=self.request.user).order_by('lead__id').first()

			if check_next_lead:
				return reverse('lead_management:lead_details', args=(check_next_lead.lead.id,))
			else:
				return reverse('lead_management:lead_details', args=(self.object.id,))
		else:
			return reverse('lead_management:lead_details', args=(self.object.id,))


	def form_valid(self,form):
		user = self.request.POST.get('user')
		obj = form.save()
		Student.objects.update_or_create(lead=obj,branch=obj.lead_task.branch,event=obj.event,defaults={'assignee_id': user})
		return super(LeadDetailsView, self).form_valid(form)


	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['title'] = "Lead Details"
	    context['lead_id'] = self.kwargs.get("pk")
	    context['check_next_lead'] = TaskAssign.objects.filter(lead__id__gt=self.object.id,assignee=self.request.user).order_by('lead__id').first()
	    context['check_prev_lead'] = TaskAssign.objects.filter(lead__id__lt=self.object.id,assignee=self.request.user).order_by('lead__id').first()
	    self.request.session['active_tab'] = 'information'
	    return context








class EventAnalysisChart(LoginRequiredMixin,View):
	def get(self,request,*args,**kwargs):
		event_id = self.kwargs.get('event_id');
		qs = TaskAssign.objects.filter(event_id=event_id).values('assignee__username').annotate(dcount=Count('assignee'))

		# html = render_to_string('accounts/super_user/chart/_event_analysis.html', {'event_data': qs})
		return JsonResponse(list(qs), safe=False)
