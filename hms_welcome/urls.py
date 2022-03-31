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
    path('verify', views.otp, name='verify'), #OTP Authentication
    path('patient_insurance_statements', views.view_insurance_statements, name='patient_insurance_statements'),
    path('request_insurance_statements', views.request_insurance_statements, name='request_insurance_statements'),

    #URL patterns for lab staff
    path('labstaff_report', views.labstaff_create_report),
    path('labstaff_reportgrid', views.labstaff_view_reports),
    path('view_test_requests', views.test_request, name='viewtestrequest'),
    path('updatetestrequest/<int:id>/<action>', views.labstaff_update_request, name='updatetestrequest'),

    #URL patterns for the hospital staff
    path('patients', views.hospitalstaff_view_patients, name='patients'),
    path('patientdata/<email>', views.hospitalstaff_view_patientdata, name='patientdata'),
    path('updateappointment/<int:id>/<action>', views.hospitalstaff_update_appointment, name='updateappointment'),
    path('transactions', views.hospitalstaff_view_transactions, name='transactions'),
    path('createtransaction/<email>',views.create_transaction, name='createtransaction'),

    #URL patterns for Doctor

    path('docPtRecords',views.doctor_update_patient_records),
    path('docPtPrescription',views.create_prescription),
    path('viewPtPrescription',views.doc_patient_prescription),
    path('updatePtPrescription',views.update_prescription),
    path('doc_register',views.doc_reg),
    path('createDiagnosis',views.createDiagnosis),
    path('updateDiagnosis',views.updateDiagnosis),
    path('viewDiagnosis',views.viewDiagnosis),
    path('deleteDiagnosis',views.deleteDiagnosis),
    path('viewLabReports',views.doctor_view_testreport),

    #URL patterns for insurance staff
    path('policies', views.insurance_staff_view_policies, name='policies'),
    path('new_policy', views.insurance_staff_new_policy, name='new_policy'),
    path('ins_staff_view_statements', views.insurance_staff_view_statements, name='ins_staff_view_statements'),
    path('update_insurance_statement/<int:id>/<action>', views.insurance_staff_approve_deny_statement, name='update_insurance_statement')
]
