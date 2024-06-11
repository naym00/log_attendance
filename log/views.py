from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from log import models as MODEL_LOGG
from help.common.generic import Generichelps as ghelp
from log.serializer import serializers as SRLZER_LOGG

@api_view(['GET'])
def getLog(request):
    employee = request.data.get('employee')
    date = request.data.get('date')
    logs = MODEL_LOGG.Log.objects.all()
    if employee: logs = logs.filter(employee=employee)
    if date: logs = logs.filter(date=date)
    logserializers = SRLZER_LOGG.Logserializer(logs, many=True)
    return Response({'data':logserializers.data, 'message': []}, status=status.HTTP_200_OK)

@api_view(['POST'])
def addLog(request):
    logserializers = SRLZER_LOGG.Logserializer(data=request.data, many=False)
    if logserializers.is_valid():
        logserializers.save()
        return Response({'data':logserializers.data, 'message': []}, status=status.HTTP_201_CREATED)
    else:  return Response({'data':logserializers.errors, 'message': []}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def updateLog(request, logid=None):
    log = MODEL_LOGG.Log.objects.filter(id=logid)
    if log.exists():
        log = log.first()
        logserializers = SRLZER_LOGG.Logserializer(instance=log, data=request.data, partial=True)
        if logserializers.is_valid():
            logserializers.save()
            return Response({'data':logserializers.data, 'message': []}, status=status.HTTP_200_OK)
        else:  return Response({'data':logserializers.errors, 'message': []}, status=status.HTTP_400_BAD_REQUEST)
    else:  return Response({'data':{}, 'message': ['doesn\'t exist!']}, status=status.HTTP_400_BAD_REQUEST)