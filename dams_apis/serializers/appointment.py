# appointment_serializer.py
from rest_framework import serializers
from django.db import IntegrityError
from dams_apis.models import Appointment, Doctor

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

    def validate(self, data):
        doctor_id = data.get('doctor').id
        appointment_date = data.get('appointment_date')

        if Appointment.objects.filter(doctor_id=doctor_id, appointment_date=appointment_date).exists():
            raise serializers.ValidationError("An appointment already exists for this date and doctor.")
        
        return data

    def create(self, validated_data):
        """Create a single appointment."""
        doctor = validated_data.get('doctor')
        appointment_date = validated_data.get('appointment_date')
        
        # Create a single appointment record
        appointment = Appointment(
            doctor=doctor,
            doctor_first_name=doctor.first_name,
            doctor_last_name=doctor.last_name,
            appointment_date=appointment_date
        )
        
        try:
            appointment.save()
        except IntegrityError:
            raise serializers.ValidationError("An appointment already exists for this date and doctor.")
        
        return appointment
