from audioop import add
from django.urls import path
from . import views

urlpatterns = [
    path("", views.login),
    #path("home",views.home,name="home"),
    path('register',views.register, name='register'),
    path('patient_profile',views.patient_profile, name="patient_profile"),
    path('logout', views.logout, name='logout'),
    path('changepassword',views.changepassword, name='changepassword'),
    path('mallogin/<uname>', views.malicious_login_otp, name='mallogin'),
    
    path('patient_prescription', views.patient_prescription, name='patient_prescription'),
    path('makeappointment', views.patient_make_appointment, name="makeappointment"),
    path('patientviewappointments', views.patient_view_appointments, name='appointments'),
    path('patient_diagnosis', views.patient_view_diagnosis, name='patient_diagnosis'),
    path('patient_testreport', views.patient_view_testreport, name='patient_testreport'),
    path('patient_view_tests', views.patient_view_tests,name='tests'),
    path('patient_request_test/<int:id>',views.patient_request_test,name='requesttest'),
    path('verify', views.otp, name='verify'), #OTP Authentication
    path('patient_insurance_statements', views.view_insurance_statements, name='patient_insurance_statements'),
    path('request_insurance_statements', views.request_insurance_statements, name='request_insurance_statements'),
    path('patient_request_reports', views.patient_request_reports, name='patient_request_reports'),

    #URL patterns for lab staff
    path('labstaff_report', views.labstaff_create_report, name="labstaff_report"),
    path('labstaff_reportgrid', views.labstaff_view_reports, name='labstaff_reportgrid'),
    path('labstaff_diagnosisgrid', views.labstaff_view_patient_diagnosis,name='diagnosisgrid'),
    path('view_test_requests', views.test_request, name='viewtestrequest'),
    path('updatetestrequest/<int:id>/<action>', views.labstaff_update_request, name='updatetestrequest'),

    #URL patterns for the hospital staff
    path('patients', views.hospitalstaff_view_patients, name='patients'),
    path('patientdata/<email>', views.hospitalstaff_view_patientdata, name='patientdata'),
    path('updateappointment/<int:id>/<action>', views.hospitalstaff_update_appointment, name='updateappointment'),
    path('transactions', views.hospitalstaff_view_transactions, name='transactions'),
    path('createtransaction/<email>',views.create_transaction, name='createtransaction'),

    #URL patterns for Doctor

    path('docPtRecords',views.doctor_update_patient_records, name="docPtRecords"),
    path('docPtPrescription',views.create_prescription, name="docPtPrescription"),
    path('viewPtPrescription',views.doc_patient_prescription, name="viewPtPrescription"),
    path('updatePtPrescription/<int:id>/',views.update_prescription, name="updatePtPrescription"),
    path('doc_register',views.doc_reg, name="doc_register"),
    path('createDiagnosis',views.createDiagnosis, name="createDiagnosis"),
    path('updateDiagnosis/<int:id>/',views.updateDiagnosis, name="updateDiagnosis"),
    path('viewDiagnosis',views.viewDiagnosis, name="viewDiagnosis"),
    path('deleteDiagnosis/<int:id>/',views.deleteDiagnosis, name="deleteDiagnosis"),
    path('viewLabReports',views.doctor_view_testreport, name="viewLabReports"),

    #URL patterns for insurance staff
    path('policies', views.insurance_staff_view_policies, name='policies'),
    path('new_policy', views.insurance_staff_new_policy, name='new_policy'),
    path('ins_staff_view_statements', views.insurance_staff_view_statements, name='ins_staff_view_statements'),
    path('update_insurance_statement/<int:id>/<action>', views.insurance_staff_approve_deny_statement, name='update_insurance_statement'),
    path('insurance_staff_create_statement', views.insurance_staff_create_statement, name='insurance_staff_create_statement'),

    #URL patterns for admin
    path('admin_transactions', views.admin_transactions, name='admin_transactions'),
    path('admin_update_transaction/<int:id>/<action>', views.admin_approve_deny_transaction, name='admin_update_transaction'),
    path('admin_update_insurance_policies', views.admin_update_insurance_policies, name='admin_update_insurance_policies'),
    path('admin_delete_insurance_policy/<int:id>/', views.admin_delete_insurance_policy, name='admin_delete_insurance_policy'),
    path('admin_create_transaction', views.admin_create_transaction, name='admin_create_transaction'),
    path('update_transaction/<int:id>/', views.update_transaction, name='update_transaction'),
    path('admin_delete_insurance_statement/<int:id>/', views.admin_delete_insurance_statement, name='admin_delete_insurance_statement'),
    path('admin_update_insurance_statement/<int:id>/', views.admin_update_insurance_statement, name='admin_update_insurance_statement'),
    path('admin_delete_prescription', views.admin_delete_prescription, name='admin_delete_prescription'),
    path('admin_create_test', views.admin_create_test, name='admin_create_test'),
    path('admin_delete_test', views.admin_delete_test, name='admin_delete_test'),
    path('admin_update_test', views.admin_update_test, name='admin_update_test'),
    path('admin_delete_appointment/<int:id>/', views.admin_delete_appointment, name='admin_delete_appointment'),
    path('admin_update_appointment/<int:id>/', views.admin_update_appointment, name='admin_update_appointment'),
    path('admin_delete_test_request/<int:id>/', views.admin_delete_test_request, name='admin_delete_test_request'),
    path('admin_update_test_request/<int:id>/', views.admin_update_test_request, name='admin_update_test_request'),
    path('admin_delete_prescription/<int:id>/', views.admin_delete_prescription, name='admin_delete_prescription'),
    
    path('admin_employee_records', views.admin_view_employees,name='viewemployees'),
    path('admin_add_employee',views.admin_add_employee,name='addemployee'),
    path('admin_update_employee/<int:id>/<action>',views.admin_update_employee,name='updateemployee'),
    path('admin_view_logs', views.admin_view_logs,name='viewlogs')
]
