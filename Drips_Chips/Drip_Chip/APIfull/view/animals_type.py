from rest_framework import viewsets
from ..Authentication import BasicAuthentications
from ..models import AnimalsType
from ..permissions import IsAuthenticatedOrReadOnly
from ..part_API import animals_types, custom_mixins
from ..serializers import AnimalsTypeRetrieveSerializer


class AnimalTypeAPI(animals_types.AnimalTypeCreate,
                    animals_types.AnimalTypeDelete,
                    animals_types.AnimalTypeUpdate,
                    custom_mixins.Retrieve,
                    viewsets.GenericViewSet):
    authentication_classes = [BasicAuthentications]
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializers_retrieve = AnimalsTypeRetrieveSerializer
    models = AnimalsType