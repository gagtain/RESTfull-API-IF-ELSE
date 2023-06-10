from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible
from rest_framework import status
from rest_framework.exceptions import ParseError, APIException
from rest_framework.response import Response

def Natural_number(number_list, err):
    if None in number_list:
        raise ParseError({'errors': err+' или отсутствует'})

    if len([number for number in number_list if number <= 0]):
        raise ParseError({'errors': err})
    else:
        return True


def create_valid(error , ser):
    if 'Недопустимый первичный ключ' in error:
        if '"0' in error or '"-' in error:  # проблема невалидности
            return Response(serializer_is_quotation_mark(ser).errors ,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer_is_quotation_mark(ser).errors, status=status.HTTP_404_NOT_FOUND)

    else:
        return Response(serializer_is_quotation_mark(ser).errors, status=status.HTTP_400_BAD_REQUEST)

@deconstructible
class No_equal_to(BaseValidator):
    message = "Убедитесь, что это значение больше %(limit_value)s."
    code = "min_value"

    def compare(self, a, b):
        return a <= 0

@deconstructible
class locations_validate(BaseValidator):
    message = "Убедитесь, что это значение меньше %(limit_value)s и больше -%(limit_value)s."
    code = "min_value"

    def compare(self, a, b):
        return not (-b <= a <= b)


def serializer_is_quotation_mark(ser):
    for n, i in enumerate(ser.errors):
        ser.errors[i][0] = ser.errors[i][0].replace('"', '')
    return ser


class The_object_already_exists(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_code = 'The_object_already_exists'