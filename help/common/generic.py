from rest_framework import status
from datetime import datetime
class Generichelps:

    def checkFields(self, classOBJ, data, allow_fields=[], required_fields=[], unique_fields=[]):
        error_message = []
        filtered_values = {}
        filtered_keys = []
        return_data = {}

        for allow_field in allow_fields:
            field_value = data.get(allow_field)
            if field_value:
                filtered_values.update({allow_field: {allow_field: field_value}})
                return_data.update({allow_field: field_value})
                filtered_keys.append(allow_field)

        for required_field in required_fields:
            if required_field not in filtered_keys: error_message.append(f'{required_field} is required!')

        for unique_field in unique_fields:
            if unique_field in filtered_keys:
                if classOBJ.objects.filter(**filtered_values[unique_field]).exists():
                    error_message.append(f'{unique_field} is already exist!')

        return {
            'error_message': error_message,
            'return_data': return_data
        }
    
    def addrecord(self, classSRLZER, data):
        response_data = {}
        response_successflag = 'error'
        response_status = status.HTTP_400_BAD_REQUEST
        print(data)
        if not data['error_message']:
            classsrlzer = classSRLZER(data['return_data'], many=False)
            print(classsrlzer)
            input()
            if classsrlzer.is_valid():
                try:    
                    classsrlzer.save()
                    response_data = classsrlzer.data
                    response_successflag = 'success'
                    response_status = status.HTTP_201_CREATED
                except:
                    data['response_message'].append('unique combination is already exist!')
            else:
                for key, value in classsrlzer.errors.items():
                    for eachvalue in value:
                        if eachvalue.code == 'required': data['response_message'].append(f'{key} (required.)')
                        elif eachvalue.code == 'invalid': data['response_message'].append(f'{key} ({eachvalue})')
                        else: data['response_message'].append(f'{key} ({eachvalue})')

        return {
            'response_data': response_data,
            'response_successflag': response_successflag,
            'response_status': response_status,
            'response_message': data['response_message']
        }
    
    def convert_STR_y_m_d_h_m_s_Dateformat(self, date_time):
        return datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
    
    def getSeconds(self, fromtime, totime):
        diff = None
        if fromtime>totime: diff = fromtime-totime
        else: diff = totime-fromtime
        return diff.seconds if diff else 0
    
    # def getShift(self, shifts, intime, outtime):
    #     selected_shift = None
    #     for shift in shifts:
    #         shift_start_at = shift.mstart_at
    #         shift_end_at = shift.mend_at
    #         print(shift_start_at)
    #         print(shift_end_at)

    def getShiftandDetails(self, shifts, first_check_in_time, last_check_out_time):
        shiftdetails = []
        # 2024-03-13 04:27:55+00:00
        selectedshift = None
        max_shift_percentage = -1

        for shift in shifts:
            
            splitdate = f'{first_check_in_time}'.split(' ')[0]
            beginning = self.convert_STR_y_m_d_h_m_s_Dateformat(f'{splitdate} {shift.mstart_at}')
            beginning_diff = (first_check_in_time - beginning).total_seconds()
            beginning_flag = True if beginning_diff<=0 else False

            # beginning_flag
            # True hole age asche =
            # False hole pore asche

            splitdate = f'{last_check_out_time}'.split(' ')[0]
            ending = self.convert_STR_y_m_d_h_m_s_Dateformat(f'{splitdate} {shift.mend_at}')
            ending_diff = (last_check_out_time - ending).total_seconds()
            ending_flag = False if ending_diff<0 else True

            # ending_flag
            # True hole pore cholegeche
            # False hole age chole geche =

            is_left_before_beginning_time = (last_check_out_time-beginning).total_seconds()
            is_enter_before_ending_time = (ending-first_check_in_time).total_seconds()
            
            if beginning_flag and ending_flag:
                if is_left_before_beginning_time>0:
                    if is_enter_before_ending_time>0:
                        percentage = 100
                        if max_shift_percentage<percentage:
                            max_shift_percentage = percentage
                            selectedshift = shift
                        shiftdetails.append({'shift': shift, 'status': 'TT', 'percentage': percentage})
            if beginning_flag and not ending_flag:
                if is_left_before_beginning_time>0:
                    if is_enter_before_ending_time>0:
                        diff = abs((last_check_out_time - beginning).total_seconds())
                        shift_diff = abs((beginning - ending).total_seconds())

                        percentage = (diff/shift_diff)*100
                        if max_shift_percentage<percentage:
                            max_shift_percentage = percentage
                            selectedshift = shift
                        shiftdetails.append({'shift': shift, 'status': 'TF', 'percentage': percentage})
            if not beginning_flag and ending_flag:
                if is_left_before_beginning_time>0:
                    if is_enter_before_ending_time>0:
                        diff = abs((first_check_in_time - ending).total_seconds())
                        shift_diff = abs((beginning - ending).total_seconds())

                        percentage = (diff/shift_diff)*100
                        if max_shift_percentage<percentage:
                            max_shift_percentage = percentage
                            selectedshift = shift
                        shiftdetails.append({'shift': shift, 'status': 'FT', 'percentage': percentage})
            if not beginning_flag and not ending_flag:
                if is_left_before_beginning_time>0:
                    if is_enter_before_ending_time>0:
                        
                        percentage = 100
                        if max_shift_percentage<percentage:
                            max_shift_percentage = percentage
                            selectedshift = shift
                        shiftdetails.append({'shift': shift, 'status': 'FF', 'percentage': percentage})
        
        return selectedshift, shiftdetails

    def calculateShiftDetails(self, shifts, first_check_in_time, last_check_out_time):


        first_check_in_time = f'{first_check_in_time}'.split('+')[0]
        first_check_in_time = f'{first_check_in_time}'[:-2] + '00'
        first_check_in_time = self.convert_STR_y_m_d_h_m_s_Dateformat(first_check_in_time)

        last_check_out_time = f'{last_check_out_time}'.split('+')[0]
        last_check_out_time = f'{last_check_out_time}'[:-2] + '00'
        last_check_out_time = self.convert_STR_y_m_d_h_m_s_Dateformat(last_check_out_time)


        delay=late=overtime=earlyleave=total_work_time = None
        shift, shift_details = self.getShiftandDetails(shifts, first_check_in_time, last_check_out_time)
        # if shift:
        #     delay = self.calculatedelay(shift, first_check_in_time)
        #     late = self.calculatelate(shift, first_check_in_time)
        #     overtime = self.calculateovertime(shift, last_check_out_time) if last_check_out_time != None else 0
        #     earlyleave = self.calculateeralyleave(shift, last_check_out_time) if last_check_out_time != None else 0
        #     # total_work_time = self.calculatetotalworktime(first_check_in_time, last_check_out_time, shift, delay, earlyleave, calculate_in_second)
        
        # total_work_time = abs((last_check_out_time - first_check_in_time).total_seconds())

        # return shift, delay, late, overtime, earlyleave, total_work_time
        return shift, shift_details