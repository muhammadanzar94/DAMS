from rest_framework import serializers
from dams_apis.models import Doctor

class DoctorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Doctor
        fields = '__all__'

    def validate(self, data):
        # Custom validation logic for doctor fields, if any
        # For example, check that names are not empty
        if not data.get('first_name'):
            raise serializers.ValidationError("First name is required.")
        if not data.get('last_name'):
            raise serializers.ValidationError("Last name is required.")
        
        return data

    def create(self, validated_data):
        # Any custom creation logic if needed
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Any custom update logic if needed
        return super().update(instance, validated_data)
