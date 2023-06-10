from django.core.exceptions import FieldError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..custom_get import get_object_or_404
from ..custom_valid import Natural_number
from ..filter_up import filter_up

# кастомный retrieve который принимает модель и сериализатор
class Retrieve(APIView):
    def retrieve(self, request, pk):
        Natural_number([pk], 'id %s <= 0' % self.models.__name__)
        obj = get_object_or_404(self.models, id=pk)
        return Response(self.serializers_retrieve(obj).data, status=status.HTTP_200_OK)

# кастомный фильтр для объектов и полей объектов
class Filter(APIView):
    # для объекта
    def search(self, request):
        req, size, froms = self.filter_val(request.GET)
        if len(req) == 0:
            q = self.models.objects.all()[froms:size + froms]
            serializer = self.serializers_retrieve(q, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        filters = self.filter_req(req)
        try:
            q = self.models.objects.filter(**filters)
        except FieldError:
            return Response(data={'errors': 'передано неверное имя поля'}, status=status.HTTP_400_BAD_REQUEST)
        q = q.order_by('id')
        ser = self.serializers_retrieve(q[froms:size + froms],many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    # для поля объекта
    def search_in_obj(self, request, pk):
        req, size, froms = self.filter_val(request.GET)
        obj = get_object_or_404(self.models, id=pk)
        List = self.get_filter_field(obj)
        if len(req) == 0:
            q = List.all().order_by('id')[froms:size + froms]
            serializer = self.serializers_retrieve(q, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        filters = self.filter_req(req)
        try:
            q = List.filter(**filters)
        except FieldError:
            return Response(data={'errors': 'передано неверное имя поля или невалидный формат поля'},
                            status=status.HTTP_400_BAD_REQUEST)
        q = q.order_by('id')
        ser = self.serializers_retrieve(q[froms:size + froms],many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    def filter_val(self, requestGET):
        filter_upe = filter_up(dict(requestGET))
        if type(filter_upe) != list:
            return filter_upe
        req = filter_upe[0]
        size = filter_upe[1]
        froms = filter_upe[2]
        return req, size, froms

    # из формата {'key': [value]} -> {'key': value}, и добаление параметров поиска
    def filter_req(self, req):
        filters = {}
        for key, value in req.items():
            if key in list(self.filter_options):
                filters[self.filter_options[key]] = req[key][0]
            else:
                filters[key] = req[key][0]
        return filters