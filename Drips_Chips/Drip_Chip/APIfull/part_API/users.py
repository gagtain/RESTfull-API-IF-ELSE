from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..Authentication import getAccountObjects
from ..custom_get import get_object_or_403
from ..custom_valid import Natural_number
from ..models import MyUser
from ..serializers import UserRetrieveSerializer, UserSerializer

# удаление юзера
class UserDelete(APIView):
    def destroy(self, request, pk):
        Natural_number([pk], {'errors': 'id аккаунта <= 0'})
        user = getAccountObjects(request)
        if user.id != pk:
            return Response(data={'errors':'Нельзя удалять не свой аккаунт'},status=status.HTTP_403_FORBIDDEN)
        if len(user.chipperID.all()) == 0:
            user.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(data={'errors':'Нельзя удалять аккаунт у которого есть чипированные животные'},
                            status=status.HTTP_400_BAD_REQUEST)

# изменение юзера
class UserUpdate(APIView):

    def update(self, request, pk):
        Natural_number([pk], {'errors': 'id аккаунта <= 0'})
        user = get_object_or_403(MyUser, id=pk)
        if getAccountObjects(request) == user:
            ser = UserSerializer(data=request.data, instance=user)
            if ser.is_valid():
                ser.update(validated_data=ser.validated_data, instance=user)
                serializer = UserRetrieveSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                if 'unique' in str(ser.errors):
                    return Response(ser.errors,status=status.HTTP_409_CONFLICT)
                return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'errors':'Нельзя редактировать не свой аккаунт'},status=status.HTTP_403_FORBIDDEN)


class UserCreate(APIView):

    # создание юзера
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.create(serializer.validated_data)
            return Response(UserRetrieveSerializer(user).data, status=status.HTTP_201_CREATED)
        else:
            if 'unique' in str(serializer.errors):
                return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)