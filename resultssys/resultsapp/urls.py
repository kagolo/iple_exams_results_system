from django.urls import path
from . import views

urlpatterns = [
    path('',views.manage_iple,name="iple"),
    path('Registration',views.manage_registration,name="registration"),
    path('Schools',views.manage_schools,name="schools"),

]