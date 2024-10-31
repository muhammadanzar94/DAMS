# urls.py
from django.urls import path
from .views.doctor_views import DoctorView
from .views.appointment_views import AppointmentView

urlpatterns = [
    # Doctor Endpoints
    path('doctors/', DoctorView.as_view()),  # GET and POST
    path('doctors/<int:doctor_id>/', DoctorView.as_view()),  # PUT and DELETE

    # Appointment Endpoints
    path('appointments/', AppointmentView.as_view(), name='appointments'),  # POST, GET for all doctors' appointments, GET for specific appointment (with date query param)
    path('appointments/<str:date>/', AppointmentView.as_view(), name='appointment_operations'),  # PUT and DELETE by appointment date
]
