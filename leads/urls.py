from django.urls import path
from .views import *

app_name="leads"

urlpatterns = [
    path('', lead_list),
    path('create/', lead_create),
    path('<int:pk>', lead_detail)
]
