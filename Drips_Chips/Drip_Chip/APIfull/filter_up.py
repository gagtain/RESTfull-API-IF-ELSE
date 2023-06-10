from rest_framework.exceptions import ParseError
from .custom_valid import Natural_number

# достает параметры size, from ил request.GET и проверяет их
def filter_up(requestGET: dict):
    try:
        size = int(requestGET['size'][0])
        requestGET.pop('size')
        Natural_number([size], 'size <= 0')

    except KeyError:

        size = 10
    try:
        froms = int(requestGET['from'][0])
        requestGET.pop('from')
        if froms < 0:
            raise ParseError({'error': 'from < 0'})

    except KeyError:

        froms = 0
    return [requestGET, size, froms]