from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..custom_get import get_object_or_404, get_object_or_409
from ..custom_valid import Natural_number
from ..models import Animals, AnimalsType
from ..serializers import AnimalsTypeRetrieveSerializer

# обновление типа животного
class AnimalTypeUpdate(APIView):

    def update(self, request, pk):
        Natural_number([pk], 'id типа животного <= 0')
        animalsType = get_object_or_404(AnimalsType, id=pk)
        serializer = AnimalsTypeRetrieveSerializer(data=request.data, instance=animalsType)
        if serializer.is_valid():
            get_object_or_409(klass=AnimalsType, field='name', type=request.data['type'])
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# удаление типа животного
class AnimalTypeDelete(APIView):

    def destroy(self, request, pk):
        Natural_number([pk], 'id типа животного <= 0')
        animalsType = get_object_or_404(AnimalsType, id=pk)
        if not len(Animals.objects.filter(animalTypes__id=pk)):
            animalsType.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(data={'errors': 'Тип животного связан с животным '},status=status.HTTP_400_BAD_REQUEST)

# создание типа животного
class AnimalTypeCreate(APIView):
    def create(self, request):
        serializer = AnimalsTypeRetrieveSerializer(data=request.data)
        if serializer.is_valid():
            get_object_or_409(AnimalsType, 'type', type=request.data['type'])
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)