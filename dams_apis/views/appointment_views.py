from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models.doctor import Doctor
from ..models.appointment import Appointment
from ..serializers import AppointmentSerializer
from django.shortcuts import get_object_or_404

class AppointmentView(APIView):
    
    def post(self, request):

        data = request.data
        doctor_id = data['doctor_id']
        appointment_dates = data['appointment_dates']  # Could be a single date or a list of dates
        try:
            doctor = Doctor.objects.get(pk=doctor_id)
        except Doctor.DoesNotExist:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

        # Create multiple appointments if necessary
        try:
            appointments = []
            if isinstance(appointment_dates, list):
                for date in appointment_dates:
                    appointment = Appointment(doctor=doctor, doctor_first_name=doctor.first_name, doctor_last_name=doctor.last_name, appointment_date=date)
                    appointments.append(appointment)
                Appointment.objects.bulk_create(appointments)
            else:
                appointment = Appointment(doctor=doctor, doctor_first_name=doctor.first_name, doctor_last_name=doctor.last_name, appointment_date=appointment_dates)
                appointment.save()
        except IntegrityError as e:
            return Response({'message': 'Appointment already exists for this date.'}, status=400)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message': 'Appointments created successfully'}, status=status.HTTP_201_CREATED)


    def put(self, request, date):
        new_doctor_id = request.data.get('doctor_id')
        new_doctor = get_object_or_404(Doctor, id=new_doctor_id)
        appointment = get_object_or_404(Appointment, appointment_date=date)

        try:
            appointment.doctor = new_doctor
            appointment.doctor_first_name = new_doctor.first_name
            appointment.doctor_last_name = new_doctor.last_name
            appointment.save()

            return Response({
                'status': 'success',
                'message': 'Appointment updated successfully!',
                'appointment': {
                    'appointment_id': appointment.id,
                    'new_doctor_id': appointment.doctor_id,
                    'new_doctor_first_name': appointment.doctor_first_name,
                    'new_doctor_last_name': appointment.doctor_last_name,
                    'appointment_date': appointment.appointment_date
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, date):
        try:
            appointment = get_object_or_404(Appointment, appointment_date=date)
            appointment.delete()
            return Response({'message': 'Appointment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        doctor_id = request.query_params.get('doctor_id')
        date = request.query_params.get('date')
        
        if date:
            try:
                appointment = Appointment.objects.get(appointment_date=date)
                return Response({
                    'doctor': f"{appointment.doctor_first_name} {appointment.doctor_last_name}"
                }, status=status.HTTP_200_OK)
            except Appointment.DoesNotExist:
                return Response({'message': f'No appointment found on {date}'}, status=status.HTTP_404_NOT_FOUND)
        
        elif doctor_id:
            doctor = get_object_or_404(Doctor, pk=doctor_id)
            appointments = [appt.appointment_date for appt in doctor.appointments.all()]
            return Response({
                'doctor': f"{doctor.first_name} {doctor.last_name}",
                'appointments': appointments
            }, status=status.HTTP_200_OK)
        
        else:
            doctors = Doctor.objects.prefetch_related('appointments').all()
            response_data = []
            for doctor in doctors:
                appointments = [appt.appointment_date for appt in doctor.appointments.all()]
                response_data.append({
                    'doctor': f"{doctor.first_name} {doctor.last_name}",
                    'appointments': appointments
                })
            return Response(response_data, status=status.HTTP_200_OK)
