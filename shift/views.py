from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from shift import models as MODEL_SHIF
from help.common.generic import Generichelps as ghelp
from shift.serializer import serializers as SRLZER_SHIF

@api_view(['GET'])
def getShift(request):
    shifts = MODEL_SHIF.Shift.objects.all()
    shiftserializers = SRLZER_SHIF.Shiftserializer(shifts, many=True)
    return Response({'data':shiftserializers.data, 'message': []}, status=status.HTTP_200_OK)

@api_view(['POST'])
def addShift(request):
    error_message = []

    allow_fields = ['name', 'start_at', 'end_at']
    required_fields = ['name', 'start_at', 'end_at']
    unique_fields = ['name']

    error_message = ghelp().checkFields(MODEL_SHIF.Shift, request.data, allow_fields=allow_fields, required_fields=required_fields, unique_fields=unique_fields)
    if not error_message:
        shifts = MODEL_SHIF.Shift.objects.all()
        shiftserializers = SRLZER_SHIF.Shiftserializer(shifts, many=False)
        if shiftserializers.is_valid():
            shiftserializers.save()
            return Response({'data':shiftserializers.data, 'message': []}, status=status.HTTP_201_CREATED)
        else:
            return Response({'data':shiftserializers.errors, 'message': []}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'data':{}, 'message': error_message}, status=status.HTTP_400_BAD_REQUEST)