from rest_framework import serializers
from .models import MyUser, locations, AnimalsType, Animals, AnimalsLocationVisit


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'firstName','lastName', 'email', 'password']


class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'firstName','lastName', 'email']


class LocationRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = locations
        fields = ['id', 'latitude','longitude']


class AnimalsTypeRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalsType
        fields = ['id', 'type']


class AnimalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animals
        fields = '__all__'


class AnimalsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animals
        fields = ['weight','length','height','gender','lifeStatus','chipperId','chippingLocationId','visitedLocations','deathDateTime']



class AnimalsLocationVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalsLocationVisit
        fields = ['id','dateTimeOfVisitLocationPoint', 'locationPointId']