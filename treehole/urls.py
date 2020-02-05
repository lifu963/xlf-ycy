from django.urls import path
from . import views

urlpatterns = [
    path('', views.tree, name='tree'),
    path('update_message/', views.update_message, name='update_message'),
    path('<int:message_pk>/', views.message_detail, name="message_detail"),
    path('defender/',views.defender,name="defender"),
    path('defender_for_medal/',views.defender_for_medal,name="defender_for_medal"),
]
