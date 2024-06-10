from rest_framework import status
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