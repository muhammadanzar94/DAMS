# urls.py
from django.urls import path
from .views.appointment_views import create_appointment, update_appointment, disassign_appointment, list_doctors_appointments, appointment_info, doctor_appointments
from .views.doctor_views import DoctorView

urlpatterns = [
    # Doctor Endpoints
    path('doctors/', DoctorView.as_view()),  # GET and POST
    path('doctors/<int:doctor_id>/', DoctorView.as_view()),  # PUT and DELETE

    # Appointment Endpoints
    path('appointments/create/', create_appointment, name='create_appointment'),
    path('appointments/update/<str:date>/', update_appointment, name='update_appointment'),
    path('appointments/disassign/<str:date>/', disassign_appointment, name='disassign_appointment'),
    path('doctors/appointments/', list_doctors_appointments, name='list_doctors_appointments'),
    path('appointment/<str:date>/', appointment_info, name='appointment_info'),
    path('doctor/<int:doctor_id>/appointments/', doctor_appointments, name='doctor_appointments'),   
]
