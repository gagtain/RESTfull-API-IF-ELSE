from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..custom_get import get_object_or_404, get_object_or_409
from ..custom_valid import Natural_number
from ..models import Animals, locations, AnimalsLocationVisit
from ..serializers import LocationRetrieveSerializer


class LocationDelete(APIView):

    def destroy(self, request, pk):
        Natural_number([pk], {'errors': 'id локации <= 0'})
        location = get_object_or_404(locations,id=pk)
        if not len(Animals.objects.filter(chippingLocationId__id=pk)) and\
                not len(AnimalsLocationVisit.objects.filter(locationPointId__id=pk)):
            location.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(data={'errors': 'точка локации связана с животным '},status=status.HTTP_400_BAD_REQUEST)


class LocationUpdate(APIView):

    def update(self, request, pk):
        Natural_number([pk], {'errors': 'id локации <= 0'})
        location = get_object_or_404(locations,id=pk)
        serializer = LocationRetrieveSerializer(data=request.data, instance=location)
        if serializer.is_valid():
            get_object_or_409(klass=locations, field='latitude longitude',
                              latitude=request.data['latitude'], longitude=request.data['longitude'])
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LocationCreate(APIView):
    def create(self, request):
        serializer = LocationRetrieveSerializer(data=request.data)
        if serializer.is_valid():
            get_object_or_409(klass=locations, field='latitude longitude',
                              latitude=request.data['latitude'], longitude=request.data['longitude'])
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)