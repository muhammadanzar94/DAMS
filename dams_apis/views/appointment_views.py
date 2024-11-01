from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models.doctor import Doctor
from ..models.appointment import Appointment
# from ..serializers import AppointmentSerializer
from django.shortcuts import get_object_or_404
from dams_apis.serializers import AppointmentSerializer
from rest_framework.exceptions import ValidationError

class AppointmentView(APIView):

    # Create single or multiple appointments
    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        
        if serializer.is_valid():
            doctor_id = serializer.validated_data['doctor'].id
            appointment_date = serializer.validated_data['appointment_date']
            
            try:
                serializer.create_appointments_with_dates(doctor_id, appointment_date)
                return Response({'message': 'Appointments created successfully'}, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

    # Update an appointment at a date
    def put(self, request, date):
        new_doctor_id = request.data.get('doctor_id')
        
        if not new_doctor_id:
            return Response({'error': 'Doctor ID is required for updating appointment'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = AppointmentSerializer()

        try:
            updated_appointment = serializer.update_appointment(date, new_doctor_id)
            return Response({
                'status': 'success',
                'message': 'Appointment updated successfully!',
                'appointment': updated_appointment
            }, status=status.HTTP_200_OK)
        except ValidationError as e:
            # Catches and returns the validation error message from serializer
            return Response({'status': 'error', 'message': e.detail}, status=status.HTTP_400_BAD_REQUEST)



    # Delete an appointment by date
    def delete(self, request, date):
        try:
            appointment = get_object_or_404(Appointment, appointment_date=date)
            appointment.delete()
            return Response({'message': 'Appointment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)




    # Get all appointments of a doctor 
    # Get all appointments of a date 
    # Get all appointments 
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
