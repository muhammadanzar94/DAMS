from rest_framework import serializers
from dams_apis.models import Doctor

class DoctorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Doctor
        fields = '__all__'

    # Validate doctors inputs params.
    def validate(self, data):
        if not data.get('first_name'):
            raise serializers.ValidationError("First name is required.")
        if not data.get('last_name'):
            raise serializers.ValidationError("Last name is required.")
        
        return data

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
