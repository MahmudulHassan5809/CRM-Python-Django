from django.urls import path
from . import views
from django.urls import reverse_lazy


app_name = 'students'

urlpatterns = [
   path('list/', views.StudentListView.as_view(),name='student_list'),
   path('details/<int:pk>/', views.StudentDetailView.as_view(),name='student_detail'),
   path('add-document/<int:student_id>/', views.AddStudentDocumentView.as_view(),name='add_student_document'),
]
