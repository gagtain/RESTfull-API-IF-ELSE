from ..models import locations as loc
from ..Authentication import BasicAuthentications
from ..permissions import IsAuthenticatedOrReadOnly
from ..part_API import locations, custom_mixins
from rest_framework import viewsets
from ..serializers import LocationRetrieveSerializer


class LocationAPI(custom_mixins.Retrieve,
                  locations.LocationCreate,
                  locations.LocationDelete,
                  locations.LocationUpdate,
                  viewsets.GenericViewSet):
    authentication_classes = [BasicAuthentications]
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializers_retrieve = LocationRetrieveSerializer
    models = loc



