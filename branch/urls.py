from django.urls import path
from . import views
from django.urls import reverse_lazy

from django.contrib.auth import views as auth_views

app_name = 'branch'

urlpatterns = [
    # Super Admin Urls
    path('create/', views.CreateBranchView.as_view(),name='create_branch'),
    path('update/<int:pk>/',views.BranchUpdateView.as_view(),name="branch_update"),
    path('delete/<int:pk>/',views.BranchDeleteView.as_view(),name="branch_delete"),



    path('branch-list/',views.BranchListView.as_view(),name="branch_list"),




]
