from django.urls import path
from . import views
from django.urls import reverse_lazy

from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html',
                                                  extra_context={'title': 'Logout', }), name="logout"),



    path('dashboard/', views.DashboardView.as_view(),name='dashboard'),


    # Super Admin Urls
    # path('super/user/dashboard/', views.SuperUserDashboardView.as_view(),name='superuser_dashboard'),
    path('user/add/',views.AddUserView.as_view(),name="add_user"),
    path('user/user-list/',views.UserListView.as_view(),name="user_list"),
    path('user/update/<int:pk>/',views.UserUpdateView.as_view(),name="user_update"),
    path('user/delete/<int:pk>/',views.UserDeleteView.as_view(),name="user_delete"),



    path('load/all-user/',views.load_all_user,name="load_all_user"),


    # path('/', views.SuperUserDashboardView.as_view(),name='superuser_dashboard'),


]
