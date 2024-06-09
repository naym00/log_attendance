class Generichelps:

    def checkFields(self, classOBJ, data, allow_fields=[], required_fields=[], unique_fields=[]):
        error_message = []
        filtered_values = {}
        filtered_keys = []
        for allow_field in allow_fields:
            field_value = data.get(allow_field)
            if field_value:
                filtered_values.update({allow_field: {allow_field: field_value}})
                filtered_keys.append(allow_field)

        for required_field in required_fields:
            if required_field not in filtered_keys: error_message.append(f'{required_field} is required!')

        for unique_field in unique_fields:
            if unique_field in filtered_keys:
                if classOBJ.objects.filter(**filtered_values[unique_field]).exists():
                    error_message.append(f'{unique_field} is already exist!')
        return error_message
         