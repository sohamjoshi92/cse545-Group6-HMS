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
    path('patientviewappointments', views.patient_view_appointments)
]