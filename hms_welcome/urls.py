from audioop import add
from django.urls import path
from . import views

urlpatterns = [
    path("", views.login),
    path('register',views.register),
    path('patient_profile',views.patient_profile),
    path('logout', views.logout),
    
    path('patient_prescription', views.patient_prescription),
    path('makeappointment', views.patient_make_appointment),
    path('patientviewappointments', views.patient_view_appointments),
    path('patient_diagnosis', views.patient_view_diagnosis),
    path('patient_testreport', views.patient_view_testreport),

    path('labstaff_report', views.labstaff_create_report),
    path('labstaff_reportgrid', views.labstaff_view_reports)
]