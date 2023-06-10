from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..custom_get import get_object_or_404, get_M2M_or_404
from ..custom_valid import Natural_number
from ..models import Animals, AnimalsType
from ..serializers import AnimalsSerializer

# добавление типа животного животному
class AnimalAddType(APIView):

    def create(self, request, pk, typeId):
        Natural_number([pk, typeId], {'errors': 'id животного или типа <= 0'})

        animals = get_object_or_404(Animals, id=pk)
        animalsTypes = get_object_or_404(AnimalsType, id=typeId)
        # проверка элементов в БД
        animal = animals
        animal.animalTypes.add(animalsTypes)
        animal.save()
        ser = AnimalsSerializer(animal)
        return Response(ser.data, status=status.HTTP_201_CREATED)


# удаление типа животного у животного
class AnimalDeleteType(APIView):
    def destroy(self, request, pk, typeId):
        Natural_number([pk, typeId], {'errors': 'id животного или типа <= 0'})
        animal = get_object_or_404(Animals, id=pk)
        # проверка нахождения элемента в поле
        get_M2M_or_404(animal.animalTypes, 'animalTypes', id=typeId)
        # если он единственный
        if animal.animalTypes.count() == 1:
            return Response(data={'errors': 'Нельзя удалять единственный тип животного'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            animal.animalTypes.remove(typeId)
            animal.save()
            return Response(AnimalsSerializer(animal).data, status=status.HTTP_200_OK)

# обновление типа животного
class AnimalUpdateType(APIView):
    def update(self, request, pk):
        Natural_number([pk], 'id животного <= 0')
        try:
            # проверка на числовой тип
            oldTypeId = request.data['oldTypeId']
            newTypeId = request.data['newTypeId']
        except:
            return Response(data={'errors': 'отсутствует oldTypeId или newTypeId'}, status=status.HTTP_400_BAD_REQUEST)
        animal = get_object_or_404(Animals, id=pk)
        Natural_number([oldTypeId, newTypeId], 'поле oldTypeId или newTypeId, <= 0')
        oldType = get_object_or_404(AnimalsType, id=oldTypeId)
        newType = get_object_or_404(AnimalsType, id=newTypeId)
        # если oldTypeID нету у животного
        get_M2M_or_404(animal.animalTypes, 'oldTypeId', id=oldTypeId)
        # если у животного уже есть newTypeId
        if animal.animalTypes.filter(id=newTypeId).exists():
            return Response(data={'errors': 'у животного уже есть newTypeId'}, status=status.HTTP_409_CONFLICT)
        else:
            animal.animalTypes.remove(oldType)
            animal.animalTypes.add(newType)
            animal.save()
            animalS = AnimalsSerializer(animal)
            return Response(animalS.data, status=status.HTTP_200_OK)