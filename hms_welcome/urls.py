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
    path('docPtRecords',views.doctor_update_patient_records),
    path('docPtPrescription',views.create_prescription),
    path('viewPtPrescription',views.doc_patient_prescription),
    path('updatePtPrescription',views.update_prescription),
    path('doc_register',views.doc_reg),
    path('createDiagnosis',views.createDiagnosis),
    path('updateDiagnosis',views.updateDiagnosis),
    path('viewDiagnosis',views.viewDiagnosis),
    path('deleteDiagnosis',views.deleteDiagnosis),
    path('viewLabReports',views.doctor_view_testreport)
]