# serializers/appointment_serializer.py
from rest_framework import serializers
from django.db import IntegrityError
from dams_apis.models import Appointment, Doctor

class AppointmentSerializer(serializers.ModelSerializer):
    doctor_id = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all(), source='doctor', write_only=True)
    appointment_date = serializers.ListField(child=serializers.CharField(), write_only=True)

    class Meta:
        model = Appointment
        fields = ['doctor_id', 'doctor_first_name', 'doctor_last_name', 'appointment_date']

    def get_doctor(self, doctor_id):
        """Retrieve doctor instance or raise validation error if not found."""
        try:
            return Doctor.objects.get(pk=doctor_id)
        except Doctor.DoesNotExist:
            raise serializers.ValidationError("Doctor not found")

    def validate_appointment_dates(self, doctor, dates):
        """Ensure no appointment exists for the specified doctor and dates."""
        if Appointment.objects.filter(doctor=doctor, appointment_date__in=dates).exists():
            raise serializers.ValidationError("An appointment already exists for one or more of these dates for this doctor.")
        
        return dates

    def create_appointments_with_dates(self, doctor_id, appointment_date):
        """Custom method to handle single and multiple appointment creation."""
        doctor = self.get_doctor(doctor_id)
        
        # Convert appointment_date to a list if it's a single date
        dates = appointment_date if isinstance(appointment_date, list) else [appointment_date]
        
        # Validate the dates
        self.validate_appointment_dates(doctor, dates)

        # Create separate appointments for each date
        appointments = [
            Appointment(
                doctor=doctor,
                doctor_first_name=doctor.first_name,
                doctor_last_name=doctor.last_name,
                appointment_date=date
            ) for date in dates
        ]

        # Bulk create appointments
        try:
            Appointment.objects.bulk_create(appointments)
        except IntegrityError:
            raise serializers.ValidationError("One or more appointments already exist for the selected dates.")
        
        return appointments
