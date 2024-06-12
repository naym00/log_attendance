from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta
from shift import models as MODEL_SHIF
from attendance import models as MODEL_ATTE
from help.common.generic import Generichelps as ghelp
from attendance.serializer import serializers as SRLZER_ATTE
from log import models as MODEL_LOGG
from log.serializer import serializers as SRLZER_LOGG
from django.db.models import Min, Max


@api_view(['GET'])
def getAttendance(request):
    employee = request.GET.get('employee')
    date = request.GET.get('date')
    fromdate = request.GET.get('fromdate')
    todate = request.GET.get('todate')

    attendances = MODEL_ATTE.Attendance.objects.all()
    
    if employee: attendances = attendances.filter(employee=employee)
    if date: attendances = attendances.filter(date=date)
    else:
        if fromdate and todate: attendances = attendances.filter(date__gte=fromdate, date__lte=todate)

    attendanceserializers = SRLZER_ATTE.Attendanceserializer(attendances, many=True)
    
    return Response({'data':attendanceserializers.data, 'message': []}, status=status.HTTP_200_OK)


@api_view(['POST'])
def generateAttendance(request, fromdate=None, todate=None):
    shifts = MODEL_SHIF.Shift.objects.all().order_by('mstart_at')
    if fromdate and todate:
        while fromdate<=todate:
            inlogs = MODEL_LOGG.Log.objects.filter(date=fromdate).values('employee').annotate(first_check_in=Min('mintime'))
            outlogs = MODEL_LOGG.Log.objects.filter(date=fromdate).values('employee').annotate(last_check_out=Max('mintime'))
            for inlog in inlogs:
                outlog = outlogs.get(employee=inlog['employee'])
                
                employee = inlog['employee']
                intime = inlog['first_check_in']
                outtime = outlog['last_check_out']
                
                log_in = MODEL_LOGG.Log.objects.get(employee=employee, mintime=intime)
                log_out = MODEL_LOGG.Log.objects.get(employee=employee, mintime=outtime)
                attendance = MODEL_ATTE.Attendance.objects.filter(employee=employee, intime=log_in.intime)
                shift, shift_details = ghelp().calculateShiftDetails(shifts, intime, outtime)
                
                if not attendance.exists():
                    try:
                        instance = MODEL_ATTE.Attendance()
                        instance.employee=employee
                        instance.intime=log_in.intime
                        instance.outtime=log_out.intime
                        instance.date=log_in.date
                        instance.save()

                        for shift_detail in shift_details:
                            if shift_detail['percentage']>=50:
                                instance.shift.add(shift_detail['shift'])
                    except: pass
                else:
                    attendance.update(outtime=log_out.intime)
                    for shift_detail in shift_details:
                        if shift_detail['percentage']>=50:
                            if shift_detail['shift'] not in attendance.first().shift.all():
                                attendance.first().shift.add(shift_detail['shift'])

            fromdate += timedelta(days=1)
        return Response({'data':{}, 'message': []}, status=status.HTTP_200_OK)
    else: return Response({'data':{}, 'message': ['need both formdate and todate!']}, status=status.HTTP_400_BAD_REQUEST)