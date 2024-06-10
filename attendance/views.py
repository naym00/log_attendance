from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from attendance import models as MODEL_ATTE
from help.common.generic import Generichelps as ghelp
from attendance.serializer import serializers as SRLZER_ATTE
from log import models as MODEL_LOGG
from log.serializer import serializers as SRLZER_LOGG

@api_view(['GET'])
def getAttendance(request):
    logs = MODEL_LOGG.Log.objects.all()

    for log in logs:


    logserializers = SRLZER_LOGG.Logserializer(logs, many=True)
    return Response({'data':logserializers.data, 'message': []}, status=status.HTTP_200_OK)