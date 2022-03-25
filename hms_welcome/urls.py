from audioop import add
from django.urls import path
from . import views

urlpatterns = [
    path("", views.login),
    path('register',views.register, name='register'),
    path('patient_profile',views.patient_profile),
    path('logout', views.logout, name='logout'),
    
    path('patient_prescription', views.patient_prescription),
    path('makeappointment', views.patient_make_appointment),
    path('patientviewappointments', views.patient_view_appointments, name='appointments'),
    path('patient_diagnosis', views.patient_view_diagnosis),
    path('patient_testreport', views.patient_view_testreport),
    path('patient_view_tests', views.patient_view_tests,name='tests'),
    path('patient_request_test/<int:id>',views.patient_request_test,name='requesttest'),
    path('patientviewtransactions', views.patient_view_transactions, name='viewtransactions'),

    #URL patterns for lab staff
    path('labstaff_report', views.labstaff_create_report),
    path('labstaff_reportgrid', views.labstaff_view_reports),
    path('view_test_requests', views.test_request, name='viewtestrequest'),
    path('updatetestrequest/<int:id>/<action>', views.labstaff_update_request, name='updatetestrequest'),

    #URL patterns for the hospital staff
    path('patients', views.hospitalstaff_view_patients, name='patients'),
    path('patientdata/<email>', views.hospitalstaff_view_patientdata, name='patientdata'),
    path('updateappointment/<int:id>/<action>', views.hospitalstaff_update_appointment, name='updateappointment')
]