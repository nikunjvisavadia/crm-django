from django.urls import path,include
from .views import *


app_name='agents'

urlpatterns=[
    path('',AgentListView.as_view(), name="agent-list"),
    path('create/',AgentCreateView.as_view(), name="agent-create"),
]