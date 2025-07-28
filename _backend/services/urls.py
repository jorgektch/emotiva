from django.urls import path
from . import views

urlpatterns = [
    path('requests/', views.ServiceRequestListCreateView.as_view(), name='service_request_list_create'),
    path('assignments/', views.AssignmentListView.as_view(), name='assignment_list'),
]
