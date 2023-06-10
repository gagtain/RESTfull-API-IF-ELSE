from ..Authentication import BasicAuthentications
from ..models import Animals
from ..part_API import animals, custom_mixins
from ..permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets
from ..serializers import AnimalsSerializer


class AnimalAPI(custom_mixins.Retrieve,
                animals.AnimalCreate,
                animals.AnimalDelete,
                animals.AnimalUpdate,
                custom_mixins.Filter,
                viewsets.GenericViewSet):
    authentication_classes = [BasicAuthentications]
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializers_retrieve = AnimalsSerializer
    models = Animals
    filter = Animals.objects
    filter_options = {
        'startDateTime':'chippingDateTime__gte',
        'endDateTime' : 'chippingDateTime__lte',
        'chipperId' : 'chipperId__id',
        'chippingLocationId' :'chippingLocationId__id',
                      }


