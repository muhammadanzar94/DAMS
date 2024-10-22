from django.db import models
from .doctor import Doctor

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    doctor_first_name = models.CharField(max_length=255, null=False, blank=False)
    doctor_last_name = models.CharField(max_length=255, null=False, blank=False)
    appointment_date = models.DateField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('doctor', 'appointment_date')

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.name} on {self.appointment_date}"
