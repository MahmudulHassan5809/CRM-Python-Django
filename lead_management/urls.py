from django.urls import path
from . import views
from django.urls import reverse_lazy


app_name = 'lead_management'

urlpatterns = [
    path('create/event/', views.CreateEvent.as_view(),name='create_event'),
    path('event/list/', views.EventListView.as_view(),name='event_list'),


	
    path('create/bulk-lead/', views.CreateBulkLeadView.as_view(),name='create_bulk_lead'),
	path('create/single-lead/', views.CreateSingleLead.as_view(),name='create_single_lead'),
	path('lead-list/',views.LeadListView.as_view(),name="lead_list"),
	path('lead-list/<int:event_id>/',views.LeadListView.as_view(),name="lead_list"),


	path('task/management/<int:event_id>/<str:type>', views.TaskManagementView.as_view(),name='task_management'),
    
]
