from django.urls import path
from . import views
from .views import GeneratePDF, manage_passslip


urlpatterns = [
    path('',views.manage_iple,name="iple"),
    path('Schools',views.manage_schools,name="schools"),
    path('school/<int:school_id>/',views.manage_single_school,name="school"),
    path('Passslip/<int:school_id>/',manage_passslip.as_view(),name="passslip"),
    path('Registration',views.manage_registration,name="registration"),
    path('About_us',views.manage_about_us,name="about_us"),
    path('Students',views.manage_student_in_students,name="student"),
    path("Contact",views.Manage_contact_us,name="contact"),
    path('pdf$/<int:student_id>/',GeneratePDF.as_view(), name="pdf"),
]  