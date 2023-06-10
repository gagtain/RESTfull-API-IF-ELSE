from rest_framework import viewsets
from ..Authentication import BasicAuthentications
from ..models import MyUser
from ..part_API import users, custom_mixins
from ..permissions import IsAuthenticatedOrReadOnly, IsNotAuthentications
from ..serializers import UserRetrieveSerializer


class UserAPI(custom_mixins.Retrieve,
              users.UserDelete,
              users.UserUpdate,
              custom_mixins.Filter,
              viewsets.GenericViewSet):
    authentication_classes = [BasicAuthentications]
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializers_retrieve = UserRetrieveSerializer
    models = MyUser
    filter_options = {
        'firstName':'firstName__icontains',
        'lastName' : 'lastName__icontains',
        'email' : 'email__icontains',
                      }


class RegistrationsAPI(users.UserCreate,
                       viewsets.GenericViewSet):

    authentication_classes = [BasicAuthentications]
    permission_classes = [IsNotAuthentications]