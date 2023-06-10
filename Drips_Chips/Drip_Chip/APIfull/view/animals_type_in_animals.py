from rest_framework import viewsets
from ..Authentication import BasicAuthentications
from ..permissions import IsAuthenticatedOrReadOnly
from ..part_API import animals_type_in_animals


class AnimalTypeInAnimalsAPI(animals_type_in_animals.AnimalAddType,
                    animals_type_in_animals.AnimalDeleteType,
                    animals_type_in_animals.AnimalUpdateType,
                    viewsets.GenericViewSet):
    authentication_classes = [BasicAuthentications]
    permission_classes = [IsAuthenticatedOrReadOnly]
