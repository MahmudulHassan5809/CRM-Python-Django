from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
import json

class SuperAdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser and request.user.active and request.user.user_type == 'SUPER_ADMIN':
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, "You Dont't Have Perission")
            return redirect('accounts:dashboard')