from django.urls import path
from . import views

urlpatterns = [
    path('accounts/', views.account_list_create),
    path('accounts/<uuid:account_id>/', views.account_detail),
    path('destinations/', views.destination_list_create),
    path('destinations/<int:pk>/', views.destination_detail),
    path('accounts/<uuid:account_id>/destinations/', views.get_destinations_by_account),
    path('server/incoming_data/', views.incoming_data),
]

