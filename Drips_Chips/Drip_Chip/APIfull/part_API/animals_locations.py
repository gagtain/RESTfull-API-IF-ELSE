from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..custom_get import get_object_or_404, get_M2M_or_404
from ..custom_valid import Natural_number
from ..models import Animals, locations, AnimalsLocationVisit
from ..serializers import AnimalsLocationVisitSerializer

# обновление точки локации в объекте с информацией о посещенной точке
class LocationInAnimalsUpdate(APIView):
    def update(self, request, pk):
        Natural_number([pk], {'errors': 'id животного <= 0'})
        animals = get_object_or_404(Animals, id=pk)
        try:
            visitedLocationPointId = request.data['visitedLocationPointId']
            locationes = request.data['locationPointId']
            Natural_number([locationes, visitedLocationPointId],
                           {'errors': 'visitedLocationPointId или locationPointId <= 0'})
            AnimalsVisList = animals.visitedLocations.order_by('id')
            AnimalsLocVis = get_M2M_or_404(AnimalsVisList, 'visitedLocationPointId', id=visitedLocationPointId)
            AnimalVisLocListAll = list(AnimalsVisList.all())
            LenAnimalsLocVis = len(AnimalVisLocListAll)
            location = get_object_or_404(locations, id=locationes)
            position = AnimalVisLocListAll.index(AnimalsLocVis)
            if AnimalsLocVis.locationPointId.id == locationes:
                return Response(data={'errors': 'у выбранного объекта уже установленна локация %s' % location.id},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                if position == 0:
                    if locationes == animals.chippingLocationId.id:
                        return Response(data={'errors': 'нельзя менять первую посещенную точку на точку чипирования'},
                                        status=status.HTTP_400_BAD_REQUEST)
                    if LenAnimalsLocVis > 1:
                        if self.aNv(AnimalVisLocListAll, position, location):
                            return self.updateAnimals(AnimalsLocVis, location)
                        else:
                            return Response(
                                data={'errors': 'обновление точки локации на точку, совпадающую со следующей точкой'},
                                status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return self.updateAnimals(AnimalsLocVis, location)
                if LenAnimalsLocVis == position + 1:
                    if self.aPv(AnimalVisLocListAll, position, location):
                        return self.updateAnimals(AnimalsLocVis, location)
                    else:
                        return Response(
                            data={'errors': 'обновление точки локации на точку, совпадающую с предыдущей точкой'},
                            status=status.HTTP_400_BAD_REQUEST)
                if self.aNv(AnimalVisLocListAll, position, location) and self.aPv(AnimalVisLocListAll, position,
                                                                                  location):
                    return self.updateAnimals(AnimalsLocVis, location)
                else:
                    return Response(data={
                        'errors': 'обновление точки локации на точку, совпадающую со следующей и/или с предыдущей точками'},
                        status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response(data={'errors': 'вы не передали visitedLocationPointId или locationPointId'},
                            status=status.HTTP_400_BAD_REQUEST)

    # функция получения локации животного до выбранной
    def aPv(self, AnimalsVisList, position, loc):
        if AnimalsVisList[position - 1].locationPointId == loc:
            return False
        else:
            return True

    # функция получения локации животного после выбранной
    def aNv(self, AnimalsVisList, position, loc):
        if AnimalsVisList[position + 1].locationPointId == loc:
            return False
        else:
            return True

    # обновление точки локации
    def updateAnimals(self, AnimalLocVis, location):
        AnimalLocVis.locationPointId = location
        AnimalLocVis.save()
        ser = AnimalsLocationVisitSerializer(AnimalLocVis)
        return Response(ser.data, status=200)

# удаление обьекта с информацией о посещенной точке
class LocationInAnimalsDelete(APIView):
    def destroy(self, request, pk, pointId):
        Natural_number([pk, pointId], {'errors': 'id животного или локации <= 0'})
        animals = get_object_or_404(Animals, id=pk)
        animalVisited = animals.visitedLocations
        AnimalLocVis = get_M2M_or_404(animalVisited, 'locations', id=pointId)
        animalVisitedAll = animalVisited.all()
        position = list(animalVisitedAll).index(AnimalLocVis)
        match animalVisited.count():
            case 0:
                return Response(data={'errors': 'у животного нет точек перемещения'},
                                status=status.HTTP_400_BAD_REQUEST)
            case 1:
                return self.delete_animal_loc(AnimalLoc=AnimalLocVis)
        if position != len(animalVisitedAll)-1:
            aNx = animalVisitedAll[position + 1]
            if position == 0 and aNx.locationPointId == animals.chippingLocationId:
                aNx.delete()
        return self.delete_animal_loc(AnimalLoc=AnimalLocVis)


    def delete_animal_loc(self, AnimalLoc):
        AnimalLoc.delete()
        return Response(status=status.HTTP_200_OK)

# добавление точки локации животному
class LocationInAnimalsCreate(APIView):
    def create(self, request, pk, pointId):
        Natural_number([pk, pointId], {'errors': 'id животного или локации <= 0'})
        animals = get_object_or_404(Animals, id=pk)
        point = get_object_or_404(locations, id=pointId)
        if animals.lifeStatus == 'DEAD':
            return Response(data={'errors': 'нельзя добавлять точку локации мертвому животному'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            AnimalVisLoc = animals.visitedLocations
            # если животное не ушло из точки чипирования и передают его локацию точки чипирования
            if animals.chippingLocationId.id == pointId and AnimalVisLoc.count() == 0:
                return Response(
                    data={'errors': 'животное не ушло из точки чипирования и передают его локацию точки чипирования'},
                    status=status.HTTP_400_BAD_REQUEST)
            match AnimalVisLoc.count():
                case 0:
                    return self.create_AnimalsLoc(animals, point=point)
                case _:
                    if AnimalVisLoc.last().locationPointId.id == pointId:
                        return Response(data={'errors': 'последняя посещенная точка локации равна добавляемой'},
                                        status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return self.create_AnimalsLoc(animals=animals, point=point)

    # добавление точки локации животному
    def create_AnimalsLoc(self, animals, point):
        AnimalsLocVis = AnimalsLocationVisit.objects.create(locationPointId=point)
        animals.visitedLocations.add(AnimalsLocVis)
        animals.save()
        a = AnimalsLocationVisitSerializer(AnimalsLocVis)
        return Response(a.data, status=status.HTTP_201_CREATED)
