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
	path('management/<int:event_id>/<str:type>', views.LeadManagementView.as_view(),name='lead_management'),


	path('lead-details/<int:pk>/',views.LeadDetailsView.as_view(),name="lead_details"),


    # path('lead-status/<int:lead_id>/',views.GetListStatusView.as_view(),name="get_lead_status"),
    # path('update-lead-status/<int:lead_id>/',views.LeadStatusUpdateView.as_view(),name="update_lead_status"),


    path('user/event/', views.UserEventListView.as_view(),name='user_event_list'),
    path('user/lead/<int:event_id>/', views.UserLeadListView.as_view(),name='user_lead_list'),


    path('event-analysis-chart/<int:event_id>/',views.EventAnalysisChart.as_view(),name='event_pie_chart')

]
