# views/doctor_views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models.doctor import Doctor
from ..serializers import DoctorSerializer
from django.shortcuts import get_object_or_404

# Doctor Views

@api_view(['POST'])
def create_doctor(request):
    serializer = DoctorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_doctor(request, doctor_id):
    try:
        doctor = get_object_or_404(Doctor, id=doctor_id)        
        serializer = DoctorSerializer(doctor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=400)




@api_view(['DELETE'])
def delete_doctor(request, doctor_id):
    try:
        doctor = get_object_or_404(Doctor, id=doctor_id)
        doctor.delete()
        return Response({'message': 'Doctor deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=400)


@api_view(['GET'])
def list_doctors(request):
    doctors = Doctor.objects.all()
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)