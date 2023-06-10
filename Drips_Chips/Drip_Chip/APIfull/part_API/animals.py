import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..custom_get import get_object_or_404
from ..custom_valid import Natural_number, create_valid
from ..models import  Animals
from ..serializers import  AnimalsSerializer, AnimalsUpdateSerializer


# добавление животного
class AnimalCreate(APIView):
    def create(self, request):
        Aform = AnimalsSerializer(data=request.data)
        if Aform.is_valid():
            Aform.save()
            return Response(Aform.data, status=status.HTTP_201_CREATED)
        else:
            # получение первой ошибки из списка ошибок
            error = str(list(Aform.errors.items())[0][1])
            # проверка нахождения элемента в БД
            return create_valid(error, Aform)

# удаление животного
class AnimalDelete(APIView):
    def destroy(self, request, pk):
        Natural_number([pk], 'id животно <= 0')
        animal = get_object_or_404(Animals, id=pk)

        if animal.visitedLocations.count() == 0:
            animal.delete()
            return Response(status=status.HTTP_200_OK)
        # если животное вернулось на место чипизации
        elif animal.chippingLocationId == animal.visitedLocations.last().locationPointId:
            animal.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(data={'errors': 'животное не вернулось в место чипирования'},status=status.HTTP_400_BAD_REQUEST)

# обновление полей животного
class AnimalUpdate(APIView):
    def update(self, request, pk):
        Natural_number([pk], {'errors': 'id животного <= 0'})
        animals = get_object_or_404(Animals, id=pk)
        serializer = AnimalsUpdateSerializer(data=request.data, instance=animals)
        if serializer.is_valid():
            if animals.visitedLocations.count() > 0:
                if animals.visitedLocations.all()[0].locationPointId.id == request.data['chippingLocationId']:
                    return Response(data={'errors': 'первая посещенная точка животного равна новой локации чипирования'},status=status.HTTP_400_BAD_REQUEST)
            serializer.update(instance=animals, validated_data=serializer.validated_data)
            if request.data['lifeStatus'] != 'ALIVE':
                animals.deathDateTime = datetime.datetime.utcnow()
            ser = AnimalsSerializer(animals)
            return Response(ser.data, status=status.HTTP_200_OK)
        else:
            # получение первой ошибки из списка ошибок
            error = str(list(serializer.errors.items())[0][1])
            # проверка нахождения элемента в БД
            return create_valid(error, serializer)
