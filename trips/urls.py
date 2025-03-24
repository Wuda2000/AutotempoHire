from django.urls import path
from . import views 

urlpatterns = [
    path('', views.trip_list, name='trip_list'),
    path('create/', views.create_trip, name='create_trip'),  # Duplicate entry removed
    path('trip/<int:pk>/', views.trip_detail, name='trip_detail'),
    path('trip/<int:pk>/update/', views.update_trip, name='update_trip'),
    path('<int:trip_id>/update/', views.trip_update, name='trip_update'),
    path('<int:trip_id>/delete/', views.trip_delete, name='trip_delete'),
]