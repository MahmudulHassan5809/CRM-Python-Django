from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.db.models import Prefetch
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View, generic
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.http import is_safe_url
from django.conf import settings
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash


from accounts.mixins import SuperAdminRequiredMixin

from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()





# Create your views here.


def load_all_user(request):
    all_user = User.objects.filter(active=True)
    
    return render(request, 'accounts/user_dropdown_list_options.html', {'all_user': all_user})





class LoginView(SuccessMessageMixin, LoginView):
    template_name = 'accounts/login.html'
    success_message = 'You Have Successfully LoggedIn.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context

    def render_to_response(self, context):
        if self.request.user.is_authenticated:
            return redirect('accounts:dashboard')
        return super().render_to_response(context)


class DashboardView(LoginRequiredMixin,View):
    def get(self,request,*arg,**kwargs):
        if request.user.is_superuser and request.user.active and request.user.user_type == 'SUPER_ADMIN':
            context = {
                'title' : 'SuperAdmin'
            }
            return render(request,'accounts/super_user/dashboard.html')
        elif request.user.active:
            context = {
                'title' : 'Dashboard'
            }
            return render(request,'accounts/user/dashboard.html')
        else:
            print(request.user,request.user.active,request.user.user_type)



        
        

class AddUserView(LoginRequiredMixin,SuperAdminRequiredMixin,View):
    def get(self,request,*arg,**kwargs):
        context = {
            'title' : 'Add User',
            'form' : CustomUserCreationForm()
        }

        return render(request,'accounts/super_user/user_management/add_user.html',context)

    def post(self,request,*args,**kwargs):
        form = CustomUserCreationForm(request.POST)
        context = {
            'title' : 'Add User',
            'form' : form
        }
        if form.is_valid():
            form.save()
            messages.success(request,"User Addedd Successfully")
            return redirect('accounts:user_list')
        else:
            return render(request,'accounts/super_user/user_management/add_user.html',context)


class UserListView(LoginRequiredMixin,SuperAdminRequiredMixin,generic.ListView):
    model = User
    context_object_name = 'user_list'
    template_name = 'accounts/super_user/user_management/user_list.html'
    paginate_by = 10

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'User List'
        return context


class UserUpdateView(SuccessMessageMixin,LoginRequiredMixin,SuperAdminRequiredMixin,generic.UpdateView):
    model = User
    context_object_name = 'user_obj'
    fields = ['email', 'username','user_type']
    template_name = 'accounts/super_user/user_management/update_user.html'
    success_message = 'Information Updated Successfully...'


    def get_success_url(self):
        return reverse_lazy('accounts:user_list')


    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update User'
        return context


class UserDeleteView(SuccessMessageMixin,LoginRequiredMixin,SuperAdminRequiredMixin,generic.DeleteView):
    model = User
    template_name = 'accounts/super_user/user_management/delete_user.html'
    success_message = 'Information deleted successfully!'


    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(UserDeleteView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('accounts:user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete User'
        return context

