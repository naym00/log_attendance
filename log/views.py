from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from log import models as MODEL_LOGG
from help.common.generic import Generichelps as ghelp
from log.serializer import serializers as SRLZER_LOGG

@api_view(['GET'])
def getLog(request):
    logs = MODEL_LOGG.Log.objects.all()
    logserializers = SRLZER_LOGG.Logserializer(logs, many=True)
    return Response({'data':logserializers.data, 'message': []}, status=status.HTTP_200_OK)

@api_view(['POST'])
def addLog(request):
    logserializers = SRLZER_LOGG.Logserializer(data=request.data, many=False)
    if logserializers.is_valid():
        logserializers.save()
        return Response({'data':logserializers.data, 'message': []}, status=status.HTTP_201_CREATED)
    else:  return Response({'data':logserializers.errors, 'message': []}, status=status.HTTP_400_BAD_REQUEST)