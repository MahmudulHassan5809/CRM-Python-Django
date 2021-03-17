from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.db.models import Prefetch
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View, generic


from .models import Lead,Event
from .forms import LeadCreateForm,EventCreateForm

# Create your views here.


class CreateEvent(SuccessMessageMixin,LoginRequiredMixin,generic.CreateView):
	model = Event 
	form_class = EventCreateForm
	template_name = "lead_management/event/create_event.html"
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
	template_name = "lead_management/event/event_list.html"
	paginate_by = 10
	

	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['title'] = "Create List"
	    return context



class CreateSingleLead(SuccessMessageMixin,LoginRequiredMixin,generic.CreateView):
	model = Lead 
	form_class = LeadCreateForm
	template_name = "lead_management/lead/create_lead.html"
	success_message = "Lead created successfully"


	def form_invalid(self,form):
		print(form.errors)


	def form_valid(self,form):
		country_of_interest = form.cleaned_data.get('country_of_interest')
		country_of_interest = form.cleaned_data.get('country_of_interest')
		country_of_interest =  country_of_interest.rstrip(',')
		country_of_interest_list = str(country_of_interest).split(',')
		country_of_interest_list = set(country_of_interest_list)

		tmp_list = []
		for country in country_of_interest_list:
			tmp_dict = {}
			tmp_dict["country"] = country
			tmp_list.append(tmp_dict)

		obj = form.save(commit=False)
		obj.created_by = self.request.user
		obj.country_of_interest = tmp_list
		obj.save()
		return redirect('lead_management:lead_list',obj.event_id)

	
	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['title'] = "Create Lead"
	    return context



class LeadListView(LoginRequiredMixin,generic.ListView):
	model = Lead 
	contect_object_name = "lead_list"
	template_name = "lead_management/lead/lead_list.html"
	paginate_by = 10

	def get_queryset(self,**kwargs):
		qs = super().get_queryset()

		event_id = self.kwargs.get('event_id',None)
		if event_id:
			qs = qs.filter_by_event(event_id)

		return qs
	

	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['title'] = "Lead List"
	    return context