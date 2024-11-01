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
            return Response({'status': 'error', 'message': e.detail}, status=status.HTTP_400_BAD_REQUEST)


   # Delete an appointment by date
    def delete(self, request, date):
        serializer = AppointmentSerializer()
        
        try:
            response_data = serializer.delete_appointment(date)
            return Response(response_data, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({'status': 'error', 'message': e.detail}, status=status.HTTP_404_NOT_FOUND)


    # Get appointments based on parameters i.e.
    # Get all appointments of a doctor 
    # Get all appointments of a date 
    # Get all appointments 
    def get(self, request):
        serializer = AppointmentSerializer()
        doctor_id = request.query_params.get('doctor_id')
        date = request.query_params.get('date')

        try:
            if date:
                response_data = serializer.get_appointments_by_date(date)
                return Response(response_data, status=status.HTTP_200_OK)

            elif doctor_id:
                response_data = serializer.get_appointments_by_doctor(doctor_id)
                return Response(response_data, status=status.HTTP_200_OK)

            else:
                response_data = serializer.get_all_appointments()
                return Response(response_data, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({'status': 'error', 'message': e.detail}, status=status.HTTP_404_NOT_FOUND)