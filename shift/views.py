from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from shift import models as MODEL_SHIF
from help.common.generic import Generichelps as ghelp
from shift.serializer import serializers as SRLZER_SHIF

@api_view(['GET'])
def getShift(request):
    
    "SELECT id, name, nickname, roll, gender, age, district FROM employee_employee WHERE age='10' AND (name LIKE '%jasim%' OR nickname LIKE '%jasim%') ORDER BY roll ASC LIMIT 10 OFFSET 10"
    
    details = {
        'select': ['id', 'name', 'nickname', 'roll', 'gender', 'age', 'district'],
        'from': 'employee_employee',
        'where':[
            {'values':[{'field': 'age', 'value': 10}], 'operation': '='},
            {'values':[{'field': 'name', 'value': 'jasim'}, {'field': 'nickname', 'value': 'jasim'}], 'operation': 'like'}
        ],
        'order_by': [{'field': 'roll', 'direction': '+'}],
            'limit': 10,
            'offset': 10
    }
    sql = ghelp().generatePaginationSQL(details)
    print(sql)
    
    
    shifts = MODEL_SHIF.Shift.objects.all()
    shiftserializers = SRLZER_SHIF.Shiftserializer(shifts, many=True)
    return Response({'data':shiftserializers.data, 'message': []}, status=status.HTTP_200_OK)

@api_view(['POST'])
def addShift(request):
    shiftserializers = SRLZER_SHIF.Shiftserializer(data=request.data, many=False)
    if shiftserializers.is_valid():
        shiftserializers.save()
        return Response({'data':shiftserializers.data, 'message': []}, status=status.HTTP_201_CREATED)
    else:  return Response({'data':shiftserializers.errors, 'message': []}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def updateShift(request, shiftid=None):
    shift = MODEL_SHIF.Shift.objects.filter(id=shiftid)
    if shift.exists():
        shift = shift.first()
        shiftserializer = SRLZER_SHIF.Shiftserializer(instance=shift, data=request.data, partial=True)
        if shiftserializer.is_valid():
            shiftserializer.save()
            return Response({'data':shiftserializer.data, 'message': []}, status=status.HTTP_200_OK)
        else:  return Response({'data':shiftserializer.errors, 'message': []}, status=status.HTTP_400_BAD_REQUEST)
    else:  return Response({'data':{}, 'message': ['doesn\'t exist!']}, status=status.HTTP_400_BAD_REQUEST)