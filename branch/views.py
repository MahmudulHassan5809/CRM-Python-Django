from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.db.models import Prefetch
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View, generic


from .models import Branch
from .forms import BranchCreateForm

# Create your views here.
class CreateBranchView(LoginRequiredMixin,SuccessMessageMixin,generic.CreateView):
    model = Branch
    form_class  = BranchCreateForm
    template_name = 'branch/super_user/create_branch.html'
    success_message = 'Information Created Successfully...'

    def get_success_url(self):
        return reverse_lazy('branch:branch_list')


    def get_context_data(self,**kwargs):
        context = super().get_context_data()
        context['title'] = 'Create Branch'
        return context


class BranchListView(LoginRequiredMixin,generic.ListView):
    model = Branch
    context_object_name = 'branch_list'
    paginate_by = 10
    template_name = 'branch/super_user/branch_list.html'


    def get_context_data(self,**kwargs):
        context = super().get_context_data()
        context['title'] = 'Branch List'
        return context



class BranchUpdateView(LoginRequiredMixin,generic.UpdateView):
    model = Branch
    form_class  = BranchCreateForm
    context_object_name = 'branch_obj'
    template_name = 'branch/super_user/update_branch.html'
    success_message = 'Information Updated Successfully...'

    def get_success_url(self):
        return reverse_lazy('branch:branch_list')


    def get_context_data(self,**kwargs):
        context = super().get_context_data()
        context['title'] = 'Update Branch'
        return context


class BranchDeleteView(LoginRequiredMixin,generic.DeleteView):
    model = Branch
    template_name = 'branch/super_user/branch_delete.html'
    success_message = 'Information deleted successfully!'


    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(BranchDeleteView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('branch:branch_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Branch'
        return context
