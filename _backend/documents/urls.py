from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.BackgroundCheckUploadView.as_view(), name='background_upload'),
    path('my/', views.MyDocumentsView.as_view(), name='my_documents'),
]
