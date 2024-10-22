# urls.py
from django.urls import path
from .views.doctor_views import create_doctor, update_doctor, delete_doctor, list_doctors
from .views.appointment_views import create_appointment, update_appointment, disassign_appointment, list_doctors_appointments

urlpatterns = [
    # Doctor Endpoints
    path('doctors/', list_doctors, name='list_doctors'),
    path('doctors/create/', create_doctor, name='create_doctor'),
    path('doctors/update/<int:doctor_id>/', update_doctor, name='update_doctor'),
    path('doctors/delete/<int:doctor_id>/', delete_doctor, name='delete_doctor'),

    # Appointment Endpoints
    path('appointments/create/', create_appointment, name='create_appointment'),
    path('appointments/update/<int:appointment_id>/', update_appointment, name='update_appointment'),
    path('appointments/disassign/<int:doctor_id>/<str:date>/', disassign_appointment, name='disassign_appointment'),
    path('doctors/appointments/', list_doctors_appointments, name='list_doctors_appointments'),
]
