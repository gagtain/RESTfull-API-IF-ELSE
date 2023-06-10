from ..Authentication import BasicAuthentications
from ..models import Animals
from ..part_API import animals_locations, custom_mixins
from ..permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets
from ..serializers import AnimalsLocationVisitSerializer


class AnimalLocationAPI(animals_locations.LocationInAnimalsUpdate,
                animals_locations.LocationInAnimalsDelete,
                animals_locations.LocationInAnimalsCreate,
                custom_mixins.Filter,
                viewsets.GenericViewSet):
    authentication_classes = [BasicAuthentications]
    permission_classes = [IsAuthenticatedOrReadOnly]
    models = Animals
    serializers_retrieve = AnimalsLocationVisitSerializer
    filter_options = {
        'startDateTime':'dateTimeOfVisitLocationPoint__gte',
        'endDateTime' : 'dateTimeOfVisitLocationPoint__lte',
                      }

    def get_filter_field(self, obj):
        return obj.visitedLocations