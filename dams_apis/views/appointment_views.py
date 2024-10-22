# views/appointment_views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models.doctor import Doctor
from ..models.appointment import Appointment
from ..serializers import AppointmentSerializer
from django.shortcuts import get_object_or_404

# Appointment Views

@api_view(['POST'])
def create_appointment(request):
    data = request.data
    doctor_id = data.get('doctor_id')
    appointment_dates = data.get('appointment_dates')  # Could be a single date or list of dates
    
    try:
        doctor = Doctor.objects.get(pk=doctor_id)
    except Doctor.DoesNotExist:
        return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

    # Create multiple appointments if necessary
    appointments = []
    if isinstance(appointment_dates, list):
        for date in appointment_dates:
            appointment = Appointment(doctor=doctor, appointment_date=date)
            appointments.append(appointment)
        Appointment.objects.bulk_create(appointments)
    else:
        appointment = Appointment(doctor=doctor, appointment_date=appointment_dates)
        appointment.save()

    return Response({'message': 'Appointments created successfully'}, status=status.HTTP_201_CREATED)


def update_appointment(request, appointment_id):
    if request.method == 'PUT':
        try:
            # Parse PUT data
            new_doctor_id = request.PUT.get('doctor_id')

            # Validate that the doctor exists
            new_doctor = get_object_or_404(Doctor, id=new_doctor_id)

            # Get the appointment to update
            appointment = get_object_or_404(Appointment, id=appointment_id)

            # Update the doctor for the appointment
            appointment.doctor_id = new_doctor.id
            appointment.doctor_name = new_doctor.name
            appointment.save()

            return Response({
                'status': 'success',
                'message': 'Appointment updated successfully!',
                'appointment': {
                    'appointment_id': appointment.id,
                    'new_doctor_id': appointment.doctor_id,
                    'new_doctor_name': appointment.doctor_name,
                    'appointment_date': appointment.appointment_date
                }
            }, status=200)

        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=400)

    return Response({'status': 'error', 'message': 'Invalid request method'}, status=405)

@api_view(['DELETE'])
def disassign_appointment(request, doctor_id, date):
    try:
        appointment = Appointment.objects.get(doctor_id=doctor_id, appointment_date=date)
        appointment.delete()
        return Response({'message': 'Appointment disassigned successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def list_doctors_appointments(request):
    doctors = Doctor.objects.prefetch_related('appointments').all()
    response_data = []

    for doctor in doctors:
        appointments = [appt.appointment_date for appt in doctor.appointments.all()]
        response_data.append({
            'doctor': doctor.first_name + ' ' + doctor.last_name,
            'appointments': appointments
        })
    
    return Response(response_data)