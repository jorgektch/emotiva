from django.urls import path
from . import views

urlpatterns = [
    path('', views.RatingListCreateView.as_view(), name='rating_list_create'),
]
